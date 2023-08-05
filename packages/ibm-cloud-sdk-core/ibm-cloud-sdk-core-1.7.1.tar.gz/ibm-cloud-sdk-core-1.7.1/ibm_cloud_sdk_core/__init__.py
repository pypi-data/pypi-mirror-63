# coding: utf-8
# Copyright 2019 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Classes and helper functions used by generated SDKs.

classes:
    BaseService: Abstract class for common functionality between each service.
    DetailedResponse: The object returned from successful service operations.
    IAMTokenManager: Requests and refreshes IAM tokens using an apikey, and optionally a client_id and client_secret.
    JWTTokenManager: Abstract class for common functionality between each JWT token manager.
    CP4DTokenManager: Requests and refreshes CP4D tokens given a username and password.
    ApiException: Custom exception class for errors returned from service operations.

functions:
    datetime_to_string: Serializes a datetime to a string.
    string_to_datetime: De-serializes a string to a datetime.
    date_to_string: Serializes a date to a string.
    string_to_date: De-serializes a string to a date.
    convert_model: Convert a model object into an equivalent dict.
    convert_list: Convert a list of strings into comma-separated string.
    read_external_sources: Get config object from external sources.
    get_authenticator_from_environment: Get authenticator from external sources.
"""

from .base_service import BaseService
from .detailed_response import DetailedResponse
from .iam_token_manager import IAMTokenManager
from .jwt_token_manager import JWTTokenManager
from .cp4d_token_manager import CP4DTokenManager
from .api_exception import ApiException
from .utils import datetime_to_string, string_to_datetime, read_external_sources
from .utils import date_to_string, string_to_date
from .utils import convert_model, convert_list
from .get_authenticator import get_authenticator_from_environment
