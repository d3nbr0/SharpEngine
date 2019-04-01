def get_vkid(vkid):
    return vkid


def get_nickname(vkid):
    vk_response = module.VK.API.call("users.get", {'user_ids': vkid})['response'][0]
    return vk_response['first_name']


columns = {'vkid': get_vkid, 'nickname': get_nickname}
