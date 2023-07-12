from Berimkharid.local_settings import fixedTokenAddNewAdmin, fixedTokenAddProductItem


def fixed_token_check(type, token):
    success = False
    if type == 'addNewAdmin' and token == fixedTokenAddNewAdmin:
        success = True
    if type == 'addProductItem' and token == fixedTokenAddProductItem:
        success = True
    return success
