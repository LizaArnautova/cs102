import dataclasses
import math
import time
import typing as tp

# from homework05.vkapi import config
# from homework05.vkapi.exceptions import APIError
# from homework05.vkapi.session import Session

from vkapi import config
from vkapi.exceptions import APIError
from vkapi.session import Session

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
        user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    start = Session(config.VK_CONFIG["domain"])
    fr_resp = FriendsResponse(0, [0])
    try:
        friends_list = start.get(
            "friends.get",
            params={
                "access_token": config.VK_CONFIG["access_token"],
                "v": config.VK_CONFIG["version"],
                "user_id": user_id,
                "count": count,
                "offset": offset,
                "fields": fields,
            },
        )

        fr_resp = FriendsResponse(
            friends_list.json()["response"]["count"], friends_list.json()["response"]["items"]
        )
    except:
        pass
    return fr_resp


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.
    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    start = Session(config.VK_CONFIG["domain"])
    friends_list = []

    if target_uids:
        n = ((len(target_uids) - 1) // 100) + 1
        for i in range(n):
            try:
                mutual_friends = start.get(
                    "friends.getMutual",
                    params={
                        "access_token": config.VK_CONFIG["access_token"],
                        "v": config.VK_CONFIG["version"],
                        "source_uid": source_uid,
                        "target_uid": target_uid,
                        "target_uids": ",".join(list(map(str, target_uids))),
                        "order": order,
                        "count": 100,
                        "offset": i * 100,
                    },
                )
                # print(mutual_friends.json())
                for friend in mutual_friends.json()["response"]:
                    friends_list.append(
                        MutualFriends(
                            id=friend["id"],
                            common_friends=list(map(int, friend["common_friends"])),
                            common_count=friend["common_count"],
                        )
                    )
            except:
                pass
            time.sleep(0.5)
        return friends_list

    try:
        mutual_friends = start.get(
            "friends.getMutual",
            params={
                "access_token": config.VK_CONFIG["access_token"],
                "v": config.VK_CONFIG["version"],
                "source_uid": source_uid,
                "target_uid": target_uid,
                "target_uids": target_uids,
                "order": order,
                "count": count,
                "offset": offset,
            },
        )
        friends_list.extend(mutual_friends.json()["response"])

    except:
        pass
    return friends_list


if __name__ == "__main__":
    # friends = get_friends(user_id=201856650).items
    # print(friends)
    print(get_mutual(201856650, target_uid=12141927))