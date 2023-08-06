# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RoaRequest

class ListTasksRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'eas', '2018-05-22', 'ListTasks')
		self.set_uri_pattern('/api/tasks')
		self.set_method('GET')

	def get_filter(self):
		return self.get_query_params().get('filter')

	def set_filter(self,filter):
		self.add_query_param('filter',filter)

	def get_pageSize(self):
		return self.get_query_params().get('pageSize')

	def set_pageSize(self,pageSize):
		self.add_query_param('pageSize',pageSize)

	def get_sort(self):
		return self.get_query_params().get('sort')

	def set_sort(self,sort):
		self.add_query_param('sort',sort)

	def get_pageNum(self):
		return self.get_query_params().get('pageNum')

	def set_pageNum(self,pageNum):
		self.add_query_param('pageNum',pageNum)