import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection
from awsglue.dynamicframe import DynamicFrame
import gs_now

def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
    dyf = dfc.select(list(dfc.keys())[0])
    dyf = dyf.resolveChoice(
        specs=[("rate", "cast:double")]
    )
    return DynamicFrameCollection({"CustomTransform": dyf,}, glueContext)

args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'source_database',
    'source_table',
    'silver_database',
    'silver_table',
    'gold_database',
    'gold_table'
])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

AWSGlueDataCatalog_node1786578365836 = glueContext.create_dynamic_frame.from_catalog(
    database=args['source_database'],
    table_name=args['source_table'],
    transformation_ctx="AWSGlueDataCatalog_node1786578365836"
)

CustomTransform_node1786616948121 = MyTransform(
    glueContext,
    DynamicFrameCollection(
        {"AWSGlueDataCatalog_node1786578365836": AWSGlueDataCatalog_node1786578365836},
        glueContext
    )
)

SelectFromCollection_node1786618180859 = SelectFromCollection.apply(
    dfc=CustomTransform_node1786616948121,
    key=list(CustomTransform_node1786616948121.keys())[0],
    transformation_ctx="SelectFromCollection_node1786618180859"
)

ChangeSchema_node1786578567840 = ApplyMapping.apply(
    frame=SelectFromCollection_node1786618180859,
    mappings=[
        ("base", "string", "base_currency", "string"),
        ("quote", "string", "target_currency", "string"),
        ("rate", "double", "rate", "double"),
        ("ingestion_date", "string", "date", "date")
    ],
    transformation_ctx="ChangeSchema_node1786578567840"
)

AddCurrentTimestamp_node1786599451848 = ChangeSchema_node1786578567840.gs_now(
    colName="ingestion_timestamp"
)

ChangeSchema_node1787020579961 = ApplyMapping.apply(
    frame=AddCurrentTimestamp_node1786599451848,
    mappings=[
        ("target_currency", "string", "currency_code", "string"),
        ("rate", "double", "rate", "double"),
        ("date", "date", "date", "date"),
        ("ingestion_timestamp", "timestamp", "ingestion_timestamp", "timestamp")
    ],
    transformation_ctx="ChangeSchema_node1787020579961"
)

PostgreSQL_node1786599652521 = glueContext.write_dynamic_frame.from_catalog(
    frame=AddCurrentTimestamp_node1786599451848,
    database=args['silver_database'],
    table_name=args['silver_table'],
    transformation_ctx="PostgreSQL_node1786599652521"
)

PostgreSQL_node1787020668677 = glueContext.write_dynamic_frame.from_catalog(
    frame=ChangeSchema_node1787020579961,
    database=args['gold_database'],
    table_name=args['gold_table'],
    transformation_ctx="PostgreSQL_node1787020668677"
)

job.commit()
