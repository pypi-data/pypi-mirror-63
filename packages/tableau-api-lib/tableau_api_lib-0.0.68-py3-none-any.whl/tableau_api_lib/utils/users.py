import pandas as pd
from tableau_api_lib.utils import extract_pages
# from tableau_api_lib.exceptions import InvalidParameterException


def get_all_users(conn):
    all_users = extract_pages(conn.get_users_on_site, parameter_dict={'fields': 'fields=_all_'})
    return all_users


def get_all_user_names(conn):
    all_users = get_all_users(conn)
    all_usernames = [user['name'] for user in all_users]
    return all_usernames


def get_all_user_emails(conn):
    all_users = get_all_users(conn)
    all_user_emails = [user['email'] for user in all_users]
    return all_user_emails


def get_all_user_fullnames(conn):
    all_users = get_all_users(conn)
    all_user_fullnames = [user['fullName'] for user in all_users]
    return all_user_fullnames


def get_all_user_roles(conn):
    all_users = get_all_users(conn)
    all_user_roles = [user['siteRole'] for user in all_users]
    return all_user_roles


def get_users_df(conn):
    users_df = pd.DataFrame(get_all_users(conn))
    return users_df
