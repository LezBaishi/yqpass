# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/8/28 15:12
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yuanqu2.settings")
django.setup()

from backend.account.models import Role, User, UserRole
from backend.workflow.models import CustomField, Workflow, State, Transition, WorkflowScript
from service.common.constant_service import CONSTANT_SERVICE

__author__ = 'x-zj'

"""
generate yuanqu workflow
"""

# generate demo_role
demander = Role.objects.create(name="需求方",
                               description="需求方, 申请工单角色", )
liaison = Role.objects.create(name="审核方",
                              description="接口人, 审核申请提交给施工方")
constructor = Role.objects.create(name="施工方",
                                  description="施工方, 确认链路, 部署链路")

# generate demo_user
shenqingren = User.objects.create_user('shenqingren@x-zj.cn', 'shenqingren', '!QAZ2wsx')
jiekouren = User.objects.create_user('jiekouren@x-zj.cn', 'jiekouren', '!QAZ2wsx')
chuliren = User.objects.create_user('chuliren@x-zj.cn', 'chuliren', '!QAZ2wsx')
UserRole.objects.create(user_id=shenqingren.id, role_id=demander.id)
UserRole.objects.create(user_id=jiekouren.id, role_id=liaison.id)
UserRole.objects.create(user_id=chuliren.id, role_id=constructor.id)

# generate workflow
workflow_obj = Workflow.objects.create(name="园区资源申请工作流",
                                       description="园区资源申请工作流",
                                       view_permission_check=True,
                                       display_form_str='["sn", "state_id", "relation", '
                                                        '"application_date", "creator",'
                                                        '"modifier", "open_date", "person1",'
                                                        '"phone1", "email1", "person2", "phone2",'
                                                        '"email2", "application_detail"]')
workflow_id = workflow_obj.id

# generate workflow custom_field
open_date = CustomField.objects.create(workflow_id=workflow_id,
                                       field_type_id=CONSTANT_SERVICE.FIELD_TYPE_DATE,
                                       field_key='open_date',
                                       field_name="预计开通时间",
                                       order_id=40)
person1 = CustomField.objects.create(workflow_id=workflow_id,
                                     field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                                     field_key='person1',
                                     field_name="移动方工程项目现场施工负责人",
                                     order_id=40)
phone1 = CustomField.objects.create(workflow_id=workflow_id,
                                    field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                                    field_key='phone1',
                                    field_name="移动方工程项目现场施工负责人电话",
                                    order_id=40)
email1 = CustomField.objects.create(workflow_id=workflow_id,
                                    field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                                    field_key='email1',
                                    field_name="移动方工程项目现场施工负责人邮箱",
                                    order_id=40)
person2 = CustomField.objects.create(workflow_id=workflow_id,
                                     field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                                     field_key='person2',
                                     field_name="现场监理/配合人员",
                                     order_id=40)
phone2 = CustomField.objects.create(workflow_id=workflow_id,
                                    field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                                    field_key='phone2',
                                    field_name="现场监理/配合人员电话",
                                    order_id=40)
email2 = CustomField.objects.create(workflow_id=workflow_id,
                                    field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                                    field_key='email2',
                                    field_name="现场监理/配合人员邮箱",
                                    order_id=40)

application_detail = CustomField.objects.create(workflow_id=workflow_id,
                                                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_TEXT,
                                                field_key='application_detail',
                                                field_name="申请单明细项",
                                                order_id=40, )

# generate workflow script
script = WorkflowScript.objects.create(name="测试脚本", saved_name='workflow_script/test.py')

# generate workflow states
init_state = State.objects.create(name="新建工单", workflow_id=workflow_id,
                                  type_id=1, participant_type_id=4,
                                  participant=demander.id,
                                  state_field_str='''{"title": 2, "application_date": 2,
                                                   "open_date": 2, "person1": 2, "phone1": 2,
                                                   "email1": 2, "person2": 2, "phone2": 2,
                                                   "email2": 2, "application_detail": 2
                                                   }''')
save_state = State.objects.create(name="草稿", workflow_id=workflow_id,
                                  type_id=0, participant_type_id=5,
                                  participant='creator',
                                  state_field_str='''{"sn": 2, "title": 2, "application_date": 2,
                                                   "open_date": 2, "person1": 2, "phone1": 2,
                                                   "email1": 2, "person2": 2, "phone2": 2,
                                                   "email2": 2, "application_detail": 2
                                                   }''')
shenhe_state = State.objects.create(name="审核中", workflow_id=workflow_id,
                                    type_id=0, participant_type_id=4,
                                    participant=liaison.id,
                                    state_field_str='''{"sn": 1, "title": 1, "application_date": 1,
                                                     "open_date": 1, "person1": 1, "phone1": 1,
                                                     "email1": 1, "person2": 1, "phone2": 1,
                                                     "email2": 1, "application_detail": 1
                                                     }''')
script_state = State.objects.create(name="链路分配中", workflow_id=workflow_id,
                                    type_id=0, participant_type_id=6,
                                    participant='test.py',
                                    state_field_str='''{"sn": 1, "title": 1, "application_date": 1,
                                                     "open_date": 1, "person1": 1, "phone1": 1,
                                                     "email1": 1, "person2": 1, "phone2": 1,
                                                     "email2": 1, "application_detail": 1
                                                     }''')
fenpei_state = State.objects.create(name="产家调度执行", workflow_id=workflow_id,
                                    type_id=0, participant_type_id=4,
                                    participant=constructor.id,
                                    state_field_str='''{"sn": 1, "title": 1, "application_date": 1,
                                                     "open_date": 1, "person1": 1, "phone1": 1,
                                                     "email1": 1, "person2": 1, "phone2": 1,
                                                     "email2": 1, "application_detail": 1
                                                     }''')
queren_state = State.objects.create(name="需求方确认", workflow_id=workflow_id,
                                    type_id=0, participant_type_id=4,
                                    participant=demander.id,
                                    state_field_str='''{"sn": 1, "title": 1, "application_date": 1,
                                                     "open_date": 1, "person1": 1, "phone1": 1,
                                                     "email1": 1, "person2": 1, "phone2": 1,
                                                     "email2": 1, "application_detail": 1
                                                     }''')
close_state = State.objects.create(name="关闭工单", workflow_id=workflow_id,
                                   type_id=0, participant_type_id=0,
                                   state_field_str='''{"sn": 1, "title": 1, "application_date": 1,
                                                     "open_date": 1, "person1": 1, "phone1": 1,
                                                     "email1": 1, "person2": 1, "phone2": 1,
                                                     "email2": 1, "application_detail": 1
                                                     }''')

# generate workflow transitions
save_ticket = Transition.objects.create(name="保存", workflow_id=workflow_id,
                                        source_state_id=init_state.id,
                                        destination_state_id=save_state.id)
submit_ticket = Transition.objects.create(name="提交", workflow_id=workflow_id,
                                          source_state_id=init_state.id,
                                          destination_state_id=shenhe_state.id)
sub_save_ticket = Transition.objects.create(name="保存提交", workflow_id=workflow_id,
                                            source_state_id=save_state.id,
                                            destination_state_id=shenhe_state.id)
back_ticket = Transition.objects.create(name="审核退回", workflow_id=workflow_id,
                                        source_state_id=shenhe_state.id,
                                        destination_state_id=save_state.id)
allow_ticket = Transition.objects.create(name="审批通过", workflow_id=workflow_id,
                                         source_state_id=shenhe_state.id,
                                         destination_state_id=script_state.id)
script_over = Transition.objects.create(name="脚本执行结束", workflow_id=workflow_id,
                                        source_state_id=script_state.id,
                                        destination_state_id=fenpei_state.id)
chuli_ticket = Transition.objects.create(name="调度分配完成、回复", workflow_id=workflow_id,
                                         source_state_id=fenpei_state.id,
                                         destination_state_id=queren_state.id)
chuli_back = Transition.objects.create(name="调度失败、回退", workflow_id=workflow_id,
                                       source_state_id=fenpei_state.id,
                                       destination_state_id=shenhe_state.id)
over_ticket = Transition.objects.create(name="完成", workflow_id=workflow_id,
                                        source_state_id=queren_state.id,
                                        destination_state_id=close_state.id)
zuofei_ticket = Transition.objects.create(name="作废", workflow_id=workflow_id,
                                          source_state_id=shenhe_state.id,
                                          destination_state_id=close_state.id)
