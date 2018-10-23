import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from service.common.format_response import api_response
from service.ticket.base_service import TicketBaseService


class TicketListView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        获取工单列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        username = request.user.username
        sn = request_data.get('sn', '')
        title = request_data.get('title', '')
        create_start = request_data.get('create_start', '')
        create_end = request_data.get('create_end', '')
        reverse = int(request_data.get('reverse', 1))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        workflow_id = request_data.get('workflow_id', '')
        category = request_data.get('category', 'duty')

        ticket_result_restful_list, msg = TicketBaseService.get_ticket_list(sn=sn,
                                                                            title=title,
                                                                            username=username,
                                                                            create_start=create_start,
                                                                            create_end=create_end,
                                                                            reverse=reverse,
                                                                            per_page=per_page,
                                                                            page=page,
                                                                            category=category)

        data = {}
        if ticket_result_restful_list is False:
            code, msg = 0, msg
        else:
            data = dict(value=ticket_result_restful_list,
                        per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg = 1, ''
        return api_response(code, msg, data)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        新建工单
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data_dict = json.loads(request.body.decode('utf-8'))
        # request_data_dict = request.POST.dict()
        # print(request.body)
        # print(json.loads(request.body))

        if not request_data_dict:
            return api_response(0, "post参数为空", {})
        request_data_dict['username'] = request.user.username

        new_ticket_result, msg = TicketBaseService.new_ticket(request_data_dict)

        if new_ticket_result:
            code, data = 1, {'ticket_id': new_ticket_result}
        else:
            code, data = 0, {}
        return api_response(code, msg, data)


class TicketView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        获取工单详情, 根据用户返回不同的内容
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        ticket_id = kwargs.get('pk')
        username = request.user.username
        if not username:
            return api_response(-1, "参数补全, 请提供username", '')
        result, msg = TicketBaseService.get_ticket_detail(ticket_id, username)

        if result is False:
            code, data = 0, ''
        else:
            code, data = 1, result
        return api_response(code, msg, data)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        处理工单
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # json_str = request.body.decode('utf-8')
        # request_data_dict = request.POST.dict()
        request_data_dict = json.loads(request.body.decode('utf-8'))
        request_data_dict['username'] = request.user.username
        request_data_dict['modifier'] = request.user.username
        if not request_data_dict:
            return api_response(0, "patch参数为空", {})
        # request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('pk', '')
        if not ticket_id:
            return api_response(0, "请提供工单id", {})
        result, msg = TicketBaseService.handle_ticket(ticket_id, request_data_dict)
        if result is False:
            code, data = 0, ''
        else:
            code, data = 1, dict(value=result)
        return api_response(code, msg, data)


class TicketTransition(View):
    """
    工单可以做的操作
    """

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('pk', '')
        username = request.user.username
        if not username:
            return api_response(0, "参数补全, 请提供 username", '')
        result, msg = TicketBaseService.get_ticket_transition(ticket_id, username)
        if result is False:
            code, data = 0, ''
        else:
            code, data = 1, dict(value=result)
        return api_response(code, msg, data)


class TicketFlowlog(View):
    """
    工单流转记录
    """

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('pk', '')
        username = request.user.username
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        if not username:
            return api_response(0, "参数补全, 请提供 username", '')

        result, msg = TicketBaseService.get_ticket_flow_log(ticket_id, per_page, page)

        if result:
            data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg = 1, ''
        else:
            code, data = 0, ''

        return api_response(1, msg, data)


class TicketFlowStep(View):
    """
    工单流转 step 用于显示工单当前状态的step图
    """

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('pk', '')
        username = request.user.username
        if not username:
            return api_response(0, "参数不全, 请提供username", '')

        result, msg = TicketBaseService.get_ticket_flow_step(ticket_id, username)
        if result:
            data = dict(value=result)
            code = 1
        else:
            code, data = 0, ''
        return api_response(code, msg, data)


class TicketState(View):
    """
    获取工单状态
    """

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        修改工单状态
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # json_str = request.body.decode('utf-8')
        # request_data_dict = request.POST.dict()
        request_data_dict = json.loads(request.body.decode('utf-8'))
        if not request_data_dict:
            return api_response(0, "post 参数为空", {})
        # request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('pk', '')
        username = request.user.username
        state_id = request_data_dict.get('state_id', '')
        if not username:
            return api_response(0, "参数不全, 请提供username", '')
        if not state_id:
            code, msg = 0, "请提供新的状态id"
            data = ''
        else:
            result, msg = TicketBaseService.update_ticket_state(ticket_id, state_id, username)
            if result:
                code, msg, data = 1, msg, ''
            else:
                code, msg, data = 0, msg, ''
        return api_response(code, msg, data)


class TicketAccept(View):
    """
    接单操作
    """

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        接单操作
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # json_str = request.body.decode('utf-8')
        # request_dxata_dict = request.POST.dict()
        request_data_dict = json.loads(request.body.decode('utf-8'))
        if not request_data_dict:
            return api_response(0, "post参数为空", {})
        # request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('pk', '')
        username = request.user.username
        result, msg = TicketBaseService.accept_ticket(ticket_id, username)
        if result:
            code, msg, data = 1, msg, result
        else:
            code, msg, data = 0, msg, ''
        return api_response(code, msg, data)


class TicketDeliver(View):
    """
    转单操作
    """

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        转单操作, 直接修改工单处理人, 且工单状态不变,
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # json_str = request.body.decode('utf-8')
        # request_data_dict = request.POST.dict()
        request_data_dict = json.loads(request.body.decode('utf-8'))
        if not request_data_dict:
            return api_response(0, "post 参数为空", {})
        # request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('pk', '')
        # username = request_data_dict.get('username', '')
        username = request.user.username
        target_username = request_data_dict.get('target_username', '')
        suggestion = request_data_dict.get('suggestion', '')

        result, msg = TicketBaseService.deliver_ticket(ticket_id, username, target_username, suggestion)
        if result:
            code, msg, data = 1, msg, result
        else:
            code, msg, data = 0, msg, ''
        return api_response(code, msg, data)


class TicketAddNode(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        加签,加签操作会修改工单处理人，工单状态不表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # json_str = request.body.decode('utf-8')
        # request_data_dict = request.POST.dict()
        request_data_dict = json.loads(request.body.decode('utf-8'))
        if not request_data_dict:
            return api_response(0, "post参数为空", {})
        # request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('pk')
        username = request.user.username
        target_username = request_data_dict.get('target_username', '')
        suggestion = request_data_dict.get('suggestion', '')
        result, msg = TicketBaseService.add_node_ticket(ticket_id, username, target_username, suggestion)
        if result:
            code, msg, data = 1, msg, result
        else:
            code, msg, data = 0, msg, ''
        return api_response(code, msg, data)


class TicketAddNodeEnd(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        加签处理完成,加签完成操作后工单处理人回回到之前加签发起人
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # json_str = request.body.decode('utf-8')
        # request_data_dict = request.POST.dict()
        request_data_dict = json.loads(request.body.decode('utf-8'))
        if not request_data_dict:
            return api_response(0, "post参数为空", {})
        # request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('pk')
        username = request.user.username
        suggestion = request_data_dict.get('suggestion', '')
        result, msg = TicketBaseService.add_node_ticket_end(ticket_id, username, suggestion)
        if result:
            code, msg, data = 1, msg, result
        else:
            code, msg, data = 0, msg, ''
        return api_response(code, msg, data)


class TicketDelete(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        删除工单，因为不想彻底清除工单记录，只是将删除字段置为0
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data_dict = json.loads(request.body.decode('utf-8'))
        # request_data_dict = request.POST.dict()
        if not request_data_dict:
            return api_response(0, "post 参数为空", "")
        username = request.user.username
        delete_str = request_data_dict.get('delete_str', '')
        result, msg = TicketBaseService.ticket_delete(username, delete_str)
        if result:
            code, msg, data = 1, msg, result
        else:
            code, msg, data = 0, msg, ''
        return api_response(code, msg, data)
