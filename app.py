import logging
import logging.config
import watchtower
import yaml
from flask import Flask
from flask_restful import Api, Resource
from boto3.session import Session

app = Flask(__name__)
api = Api(app)

AWS_PROFILE = 'default'
AWS_REGION_NAME = 'us-east-1'

boto3_session = Session(profile_name=AWS_PROFILE,
                        region_name=AWS_REGION_NAME)

with open('logging.yml') as log_config:
        config_yml = log_config.read()
        config_dict = yaml.safe_load(config_yml)
        config_dict['handlers']['watchtower']['boto3_session'] = boto3_session
        logging.config.dictConfig(config_dict)  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(watchtower.CloudWatchLogHandler(
    log_group='diana-logging-test',
    stream_name='test',
    boto3_session=boto3_session))
logger.info("Hi-009")

# class HelloWorld(Resource):
#     def get(self):
#         logging.info("Testing GET")
#         return {"data":"Hello World"}

# api.add_resource(HelloWorld, "/helloworld")

# if __name__ == "__main__":  
#     app.run()