from enum import Enum

class DefaultPermissions(Enum):
    VIEW_LAWYER = "view_lawyer"
    CREATE_LAWYER = "create_lawyer"
    UPDATE_LAWYER = "update_lawyer"
    DELETE_LAWYER = "delete_lawyer"
    VIEW_CUSTOMER = "view_customer"
    CREATE_CUSTOMER = "create_customer"
    UPDATE_CUSTOMER = "update_customer"
    DELETE_CUSTOMER = "delete_customer"
    VIEW_POSITION = "view_position"
    CREATE_POSITION = "create_position"
    UPDATE_POSITION = "update_position"
    DELETE_POSITION = "delete_position"
