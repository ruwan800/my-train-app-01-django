from group.functions import UsersFavouredStation, UsersAtStation,\
    UsersNearStation


def StationUsers(ref):
    users = UsersFavouredStation(ref)
    users += UsersAtStation(ref)
    users += UsersNearStation(ref)
    return list(set(users))
    