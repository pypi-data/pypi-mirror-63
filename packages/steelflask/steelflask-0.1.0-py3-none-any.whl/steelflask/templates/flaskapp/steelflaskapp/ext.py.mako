# Do not import anything from ${app_name} domain to avoid circular dependency
import os
from flask import json, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

APP_DIR = os.path.dirname(__file__)


class SfSQLAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        options['json_serializer'] = json.dumps
        super().apply_driver_hacks(app, info, options)


db = SfSQLAlchemy()
migrate = Migrate()


def Transactional(func):
    def with_transaction(*args, **kwargs):
        funct_return = func(*args, **kwargs)
        db.session.commit()
        return funct_return

    return with_transaction


class ResponseCode:
    SUCCESS = 2000
    BAD_REQUEST = 4000
    UNKNOWN_ERROR = 4010
    AUTHENTICATION_ERROR = 4020
    ORG_CONTEXT_MISSING = 4022
    AUTHENTICATION_REQUIRED = 4021
    UNAUTHORIZE = 4030
    RESOURCE_NOT_FOUND = 4040
    METHOD_NOT_ALLOWED = 4050


class ApiResponse:
    @staticmethod
    def success(message="Success", payload=None):
        response = {
            'statusCode': ResponseCode.SUCCESS,
            'message': message
        }
        if payload is not None:
            response['payload'] = payload

        return jsonify(response)

    @staticmethod
    def error(error_code=ResponseCode.UNKNOWN_ERROR, errors=None, message="Some unknown error occured."):
        response = {
            'statusCode': error_code,
            'message': message
        }
        if errors is not None:
            response['errors'] = errors
        return response


class SessionContext(object):
    def __init__(self, id, user_id, user_name, is_first_login, app_role=None,
                 selected_organisation=None, selected_opunit=None, opunit_role=None,
                 accessible_org_count=0, accessible_opunit_count=0,
                 permissions={}):
        self.id = id
        self.user_id = user_id
        self.user_name = user_name
        self.is_first_login = is_first_login
        self.app_role = app_role
        self.selected_subscription = selected_organisation
        self.subscription_role = selected_opunit
        self.accessible_sub_count = accessible_org_count
        self.permissions = permissions

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'userName': self.user_name,
            'isFirstLogin': self.is_first_login,
            'appRole': self.app_role,
            'selectedSubscription': self.selected_subscription,
            'subscriptionRole': self.subscription_role,
            'accessibleSubscriptionCount': self.accessible_sub_count,
            'permissions': self.permissions
        }
