from user_mgmt.models import UserRoles, UserGroups, UserPermissionGroups, Users
from third_party.models.third_party_models import SalesforceSync, SalesforceUserInfo


# Create User Groups
ugid_1 = UserGroups(group_name='home_loans')
ugid_1.save()
group_id_1 = ugid_1.group_id
ugid_2 = UserGroups(group_name='brand')
ugid_2.save()
group_id_2 = ugid_2.group_id
ugid_3 = UserGroups(group_name='kiosk')
ugid_3.save()
group_id_3 = ugid_3.group_id
ugid_4 = UserGroups(group_name='rbac')
ugid_4.save()
group_id_4 = ugid_4.group_id

# Create User Roles for Groups
# --- Home Loans
urid_1 = UserRoles(role_name='admin',
                   group_id=UserGroups.objects.get(group_id=group_id_1))
urid_1.save()
role_id_1 = urid_1.role_id
urid_2 = UserRoles(role_name='user',
                   group_id=UserGroups.objects.get(group_id=group_id_1))
urid_2.save()
role_id_2 = urid_2.role_id
# --- Brand
urid_3 = UserRoles(role_name='admin',
                   group_id=UserGroups.objects.get(group_id=group_id_2))
urid_3.save()
role_id_3 = urid_3.role_id
urid_4 = UserRoles(role_name='user',
                   group_id=UserGroups.objects.get(group_id=group_id_2))
urid_4.save()
role_id_4 = urid_4.role_id
# --- Kiosk
urid_5 = UserRoles(role_name='admin',
                   group_id=UserGroups.objects.get(group_id=group_id_3))
urid_5.save()
role_id_5 = urid_5.role_id
urid_6 = UserRoles(role_name='user',
                   group_id=UserGroups.objects.get(group_id=group_id_3))
urid_6.save()
role_id_6 = urid_6.role_id
urid_7 = UserRoles(role_name='admin',
                   group_id=UserGroups.objects.get(group_id=group_id_4))
urid_7.save()
role_id_7 = urid_7.role_id

# Create User Permission Groups
# --- Crete a super user initially from command group, assume user id to be 1
user_obj = Users.objects.get(user_id=1)
UserPermissionGroups(
    user_id=user_obj,
    role_id=UserRoles.objects.get(role_id=role_id_1),
    group_id=UserGroups.objects.get(group_id=group_id_1),
).save()
UserPermissionGroups(
    user_id=user_obj,
    role_id=UserRoles.objects.get(role_id=role_id_3),
    group_id=UserGroups.objects.get(group_id=group_id_2),
).save()
UserPermissionGroups(
    user_id=user_obj,
    role_id=UserRoles.objects.get(role_id=role_id_5),
    group_id=UserGroups.objects.get(group_id=group_id_3),
).save()
UserPermissionGroups(
    user_id=user_obj,
    role_id=UserRoles.objects.get(role_id=role_id_7),
    group_id=UserGroups.objects.get(group_id=group_id_4),
).save()


# Third Party SalesForce data
sf_user = SalesforceUserInfo(sf_user_id='0057F0000026rjeQAA', first_name='Santhosh', last_name='Badam',
                             email='santhosh.badam@dp.exchange')
sf_user.save()


sf_user = SalesforceUserInfo(sf_user_id='0057F0000048xZIQAY', first_name='Mark', last_name='Shwaros',
                             email='mark.shwaros@dealmax.com.au')
sf_user.save()


'0057F0000048xZIQAY'
'0057F0000026rjeQAA'