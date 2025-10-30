# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def handle_volcengine_api_error(e: Exception) -> Exception:
    """Handle Volcengine API errors
    Args:
        e: The exception that was raised

    Returns:
        Standardized ClientError with Volcengine error details
    """

    # Fallback for other exceptions
    return ClientError(f"An error occurred: {str(e)}")


class ClientError(Exception):
    """An error that indicates that the request was malformed or incorrect in some way. There was no issue on the server side."""

    def __init__(self, message):
        """Call super and set message."""
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.type = "client"
        self.message = message


class ServerError(Exception):
    """An error that indicates that there was an issue processing the request."""

    def __init__(self, message: str):
        """Initialize ServerError with message."""
        super().__init__(message)
        self.type = "server"
        self.message = message
