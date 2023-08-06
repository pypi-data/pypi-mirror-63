# -*- coding:utf-8 -*-
# Copyright 2019 Huawei Technologies Co.,Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License.  You may obtain a copy of the
# License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.

from openstack.bssintl import bss_intl_service
from openstack import resource2
from openstack import utils
try:
    # Python3
    from urllib.parse import urlencode
except ImportError:
    # Python2
    from urllib import urlencode


class QueryCustomerPeriodResourcesList(resource2.Resource):
    base_path = "%(domain_id)s/common/order-mgr/resources/detail"
    service = bss_intl_service.BssIntlService()
    allow_get = True

    # User domain ID
    domain_id = resource2.URI('domain_id')


    # request
    # Resource IDs
    resource_ids = resource2.Body('resource_ids')
    order_id = resource2.Body('order_id')
    only_main_resource = resource2.Body('only_main_resource', type=int)
    status_list = resource2.Body('status_list')
    page_no = resource2.Body('page_no', type=int)
    page_size = resource2.Body('page_size', type=int)

    # response
    #  Status code.
    error_code = resource2.Body('error_code')
    # Error description.
    error_msg = resource2.Body('error_msg')
    data = resource2.Body('data', type=list)
    total_count = resource2.Body('total_count', type=int)

    def get(self, session, requires_id=False):
        request = self._prepare_request(requires_id=False)
        endpoint_override = self.service.get_endpoint_override()
        service = self.get_service_filter(self, session)
        xstr = lambda s: '' if s is None else str(s)
        query_dict = {'resource_ids': xstr(self.resource_ids), 'order_id': xstr(self.order_id),
                      'only_main_resource': xstr(self.only_main_resource), 'status_list': xstr(self.status_list),
                      'page_no': xstr(self.page_no), 'page_size': xstr(self.page_size)}
        query_str = urlencode(query_dict, doseq=True)
        url = request.uri + "?" + query_str
        response = session.get(url, endpoint_filter=self.service,
                               microversion=service.microversion,
                               endpoint_override=endpoint_override)
        self._translate_response(response)
        return self


class RenewSubscriptionByResourceId(resource2.Resource):
    base_path = "%(domain_id)s/common/order-mgr/resources/renew"
    service = bss_intl_service.BssIntlService()
    allow_create = True

    domain_id = resource2.URI('domain_id')

    # request
    # Resource IDs.
    resource_ids = resource2.Body('resource_ids', type=list)
    # Period type.
    period_type = resource2.Body('period_type', type=int)
    # Number of periods.
    period_num = resource2.Body('period_num', type=int)
    # Expiration policy.
    expire_mode = resource2.Body('expire_mode', type=int)
    # Whether enable automatic payment.
    isAutoPay = resource2.Body('isAutoPay', type=int)

    # response
    #  Status code.
    error_code = resource2.Body('error_code')
    # Error description.
    error_msg = resource2.Body('error_msg')
    # List of order IDs generated when resource subscription is renewed.
    order_ids = resource2.Body('order_ids', type=list)


class UnsubscribeByResourceId(resource2.Resource):
    base_path = "%(domain_id)s/common/order-mgr/resources/delete"
    service = bss_intl_service.BssIntlService()
    allow_create = True

    domain_id = resource2.URI('domain_id')

    # request
    # Queries resource IDs in batches
    resourceIds = resource2.Body('resourceIds', type=list)
    # Unsubscription type.
    unSubType = resource2.Body('unSubType', type=int)
    # Unsubscription cause.
    unsubscribeReasonType = resource2.Body('unsubscribeReasonType', type=int)
    # Unsubscription reason, which is generally specified by the customer.
    unsubscribeReason = resource2.Body('unsubscribeReason')

    # response
    #  Status code.
    error_code = resource2.Body('error_code')
    # Error description.
    error_msg = resource2.Body('error_msg')
    # Unsubscription order IDs.
    orderIds = resource2.Body('orderIds', type=list)


class AutoRenew(resource2.Resource):
    base_path = "%(domain_id)s/common/order-mgr/resources/%(resource_id)s/actions?action_id=%(action_id)s"
    service = bss_intl_service.BssIntlService()
    # capabilities
    allow_update = True
    allow_delete = True

    # User domain ID
    domain_id = resource2.URI('domain_id')
    # traced resource id
    resource_id = resource2.URI('resource_id')
    action_id = resource2.URI('action_id')

    #  Status code.
    error_code = resource2.Body('error_code')
    # Error description.
    error_msg = resource2.Body('error_msg')

    def create(self, session, prepend_key=True):
        endpoint_override = self.service.get_endpoint_override()
        request = self._prepare_request(requires_id=False,
                                        prepend_key=prepend_key)
        response = session.post(request.uri, endpoint_filter=self.service,
                                endpoint_override=endpoint_override,
                                json=request.body, headers=request.headers)
        self._translate_response(response)
        return self

    def delete(self, session, params=None, has_body=False):
        endpoint_override = self.service.get_endpoint_override()
        request = self._prepare_request(requires_id=False)
        response = session.delete(request.uri, endpoint_filter=self.service,
                                  endpoint_override=endpoint_override,
                                  headers=request.headers)
        self._translate_response(response)
        return self
