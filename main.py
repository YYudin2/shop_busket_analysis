import itertools
import collections


def read_orders(file_name: str, separator: str):

    with open(file_name) as file:
        lines = file.read()
    raw_order_list = list(filter(lambda x: x != '', lines.split('\n')))
    order_list = []
    for item in raw_order_list:
        order = item.split(separator)
        order_list.append(order)
    return order_list

def calculate_stat(order_list: list, min_support: int, min_confidence: float):

    pairs_dict = {}
    unique_prod_list = list(itertools.chain.from_iterable(order_list))
    unique_products_dict = collections.Counter(unique_prod_list)
    # this and followed lower loops with del (item from dictionary) are implemented to short analyzed list to items,
    # which are only applicable to min_support, otherwise searching is very slow
    for u_prod in list(unique_products_dict.keys()):
        if unique_products_dict[u_prod] < min_support:
            del unique_products_dict[u_prod]

    for orders in order_list:
        order_comb = list(itertools.combinations(orders, 2))
        for pair in order_comb:
            if pair[0] in unique_products_dict.keys() and pair[1] in unique_products_dict.keys():
                if pair not in pairs_dict.keys():
                    pairs_dict[pair] = 1
                else:
                    pairs_dict[pair] += 1

                pair_rev = (pair[1], pair[0])
                if pair_rev not in pairs_dict.keys():
                    pairs_dict[pair_rev] = 1
                else:
                    pairs_dict[pair_rev] += 1
    # the same comment as was mentioned earlier for following loop:
    for p_prod in list(pairs_dict.keys()):
        if pairs_dict[p_prod] < min_support:
            del pairs_dict[p_prod]

    result = []
    for product in unique_products_dict:
        prod_count = unique_products_dict[product]
        for pair in pairs_dict:
            if product in pair and (pairs_dict[pair] / prod_count) > min_confidence:
                common_count = pairs_dict[pair]
                index = pair.index(product)
                product2 = pair[index - 1]
                confidence = common_count / prod_count
                result.append(f'{product} => {product2}({confidence:.2%} confidence), {common_count} support \n')
                break
            else:
                continue
    return result


nl = read_orders('orders.txt', '@@@')

print (*calculate_stat(nl, 500, 0.3))
