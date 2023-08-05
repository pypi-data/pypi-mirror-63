# -*- coding: utf8 -*-
# Copyright (c) 2017-2018 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.tcr.v20190924 import models


class TcrClient(AbstractClient):
    _apiVersion = '2019-09-24'
    _endpoint = 'tcr.tencentcloudapi.com'


    def BatchDeleteImagePersonal(self, request):
        """用于在个人版镜像仓库中批量删除Tag

        :param request: Request instance for BatchDeleteImagePersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.BatchDeleteImagePersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.BatchDeleteImagePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("BatchDeleteImagePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.BatchDeleteImagePersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def BatchDeleteRepositoryPersonal(self, request):
        """用于个人版镜像仓库中批量删除镜像仓库

        :param request: Request instance for BatchDeleteRepositoryPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.BatchDeleteRepositoryPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.BatchDeleteRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("BatchDeleteRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.BatchDeleteRepositoryPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateApplicationTriggerPersonal(self, request):
        """用于创建应用更新触发器

        :param request: Request instance for CreateApplicationTriggerPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.CreateApplicationTriggerPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.CreateApplicationTriggerPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateApplicationTriggerPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateApplicationTriggerPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateImageLifecyclePersonal(self, request):
        """用于在个人版中创建清理策略

        :param request: Request instance for CreateImageLifecyclePersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.CreateImageLifecyclePersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.CreateImageLifecyclePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateImageLifecyclePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateImageLifecyclePersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateInstance(self, request):
        """创建实例

        :param request: Request instance for CreateInstance.
        :type request: :class:`tencentcloud.tcr.v20190924.models.CreateInstanceRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.CreateInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateInstanceToken(self, request):
        """获取临时登录密码

        :param request: Request instance for CreateInstanceToken.
        :type request: :class:`tencentcloud.tcr.v20190924.models.CreateInstanceTokenRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.CreateInstanceTokenResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateInstanceToken", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateInstanceTokenResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateNamespacePersonal(self, request):
        """创建个人版镜像仓库命名空间，此命名空间全局唯一

        :param request: Request instance for CreateNamespacePersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.CreateNamespacePersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.CreateNamespacePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateNamespacePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateNamespacePersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateRepositoryPersonal(self, request):
        """用于在个人版仓库中创建镜像仓库

        :param request: Request instance for CreateRepositoryPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.CreateRepositoryPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.CreateRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateRepositoryPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateUserPersonal(self, request):
        """创建个人用户

        :param request: Request instance for CreateUserPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.CreateUserPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.CreateUserPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateUserPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateUserPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteApplicationTriggerPersonal(self, request):
        """用于删除应用更新触发器

        :param request: Request instance for DeleteApplicationTriggerPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DeleteApplicationTriggerPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DeleteApplicationTriggerPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteApplicationTriggerPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteApplicationTriggerPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteImageLifecyclePersonal(self, request):
        """用于在个人版镜像仓库中删除仓库Tag自动清理策略

        :param request: Request instance for DeleteImageLifecyclePersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DeleteImageLifecyclePersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DeleteImageLifecyclePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteImageLifecyclePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteImageLifecyclePersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteImagePersonal(self, request):
        """用于在个人版中删除tag

        :param request: Request instance for DeleteImagePersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DeleteImagePersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DeleteImagePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteImagePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteImagePersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteNamespacePersonal(self, request):
        """删除共享版命名空间

        :param request: Request instance for DeleteNamespacePersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DeleteNamespacePersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DeleteNamespacePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteNamespacePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteNamespacePersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteRepositoryPersonal(self, request):
        """用于个人版镜像仓库中删除

        :param request: Request instance for DeleteRepositoryPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DeleteRepositoryPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DeleteRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteRepositoryPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeApplicationTriggerLogPersonal(self, request):
        """用于查询应用更新触发器触发日志

        :param request: Request instance for DescribeApplicationTriggerLogPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeApplicationTriggerLogPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeApplicationTriggerLogPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeApplicationTriggerLogPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeApplicationTriggerLogPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeApplicationTriggerPersonal(self, request):
        """用于查询应用更新触发器

        :param request: Request instance for DescribeApplicationTriggerPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeApplicationTriggerPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeApplicationTriggerPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeApplicationTriggerPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeApplicationTriggerPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeFavorRepositoryPersonal(self, request):
        """查询个人收藏仓库

        :param request: Request instance for DescribeFavorRepositoryPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeFavorRepositoryPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeFavorRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeFavorRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeFavorRepositoryPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeImageFilterPersonal(self, request):
        """用于在个人版中查询与指定tag镜像内容相同的tag列表

        :param request: Request instance for DescribeImageFilterPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeImageFilterPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeImageFilterPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageFilterPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageFilterPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeImageLifecyclePersonal(self, request):
        """用于获取个人版仓库中自动清理策略

        :param request: Request instance for DescribeImageLifecyclePersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeImageLifecyclePersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeImageLifecyclePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageLifecyclePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageLifecyclePersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeImagePersonal(self, request):
        """用于获取个人版镜像仓库tag列表

        :param request: Request instance for DescribeImagePersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeImagePersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeImagePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImagePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImagePersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeInstanceStatus(self, request):
        """查询实例当前状态以及过程信息

        :param request: Request instance for DescribeInstanceStatus.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeInstanceStatusRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeInstanceStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeInstances(self, request):
        """查询实例信息

        :param request: Request instance for DescribeInstances.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeInstancesRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNamespacePersonal(self, request):
        """查询个人版命名空间信息

        :param request: Request instance for DescribeNamespacePersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeNamespacePersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeNamespacePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeNamespacePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeNamespacePersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRepositoryFilterPersonal(self, request):
        """用于在个人版镜像仓库中，获取满足输入搜索条件的用户镜像仓库

        :param request: Request instance for DescribeRepositoryFilterPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeRepositoryFilterPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeRepositoryFilterPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRepositoryFilterPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRepositoryFilterPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRepositoryOwnerPersonal(self, request):
        """用于在个人版中获取用户全部的镜像仓库列表

        :param request: Request instance for DescribeRepositoryOwnerPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeRepositoryOwnerPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeRepositoryOwnerPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRepositoryOwnerPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRepositoryOwnerPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRepositoryPersonal(self, request):
        """查询个人版仓库信息

        :param request: Request instance for DescribeRepositoryPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeRepositoryPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRepositoryPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeUserQuotaPersonal(self, request):
        """查询个人用户配额

        :param request: Request instance for DescribeUserQuotaPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DescribeUserQuotaPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DescribeUserQuotaPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUserQuotaPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserQuotaPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DuplicateImagePersonal(self, request):
        """用于在个人版镜像仓库中复制镜像版本

        :param request: Request instance for DuplicateImagePersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.DuplicateImagePersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.DuplicateImagePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DuplicateImagePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DuplicateImagePersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyApplicationTriggerPersonal(self, request):
        """用于修改应用更新触发器

        :param request: Request instance for ModifyApplicationTriggerPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.ModifyApplicationTriggerPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.ModifyApplicationTriggerPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyApplicationTriggerPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyApplicationTriggerPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyRepositoryAccessPersonal(self, request):
        """用于更新个人版镜像仓库的访问属性

        :param request: Request instance for ModifyRepositoryAccessPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.ModifyRepositoryAccessPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.ModifyRepositoryAccessPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRepositoryAccessPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRepositoryAccessPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyRepositoryInfoPersonal(self, request):
        """用于在个人版镜像仓库中更新容器镜像描述

        :param request: Request instance for ModifyRepositoryInfoPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.ModifyRepositoryInfoPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.ModifyRepositoryInfoPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRepositoryInfoPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRepositoryInfoPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyUserPasswordPersonal(self, request):
        """修改个人用户登录密码

        :param request: Request instance for ModifyUserPasswordPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.ModifyUserPasswordPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.ModifyUserPasswordPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyUserPasswordPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyUserPasswordPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ValidateNamespaceExistPersonal(self, request):
        """查询个人版用户命名空间是否存在

        :param request: Request instance for ValidateNamespaceExistPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.ValidateNamespaceExistPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.ValidateNamespaceExistPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ValidateNamespaceExistPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ValidateNamespaceExistPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ValidateRepositoryExistPersonal(self, request):
        """用于判断个人版仓库是否存在

        :param request: Request instance for ValidateRepositoryExistPersonal.
        :type request: :class:`tencentcloud.tcr.v20190924.models.ValidateRepositoryExistPersonalRequest`
        :rtype: :class:`tencentcloud.tcr.v20190924.models.ValidateRepositoryExistPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ValidateRepositoryExistPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ValidateRepositoryExistPersonalResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)