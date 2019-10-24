#pylint: disable=no-member
import tcod as libtcod
from game_messages import Message

class Inventory:
    def __init__(self, capacity):
        self.capacity=capacity
        self.contents=[]

    def add_item(self, item):
        results=[]
        if len(self.contents)>=self.capacity:
            results.append({'item_added': None, 'message': Message('Your inventory is full.', libtcod.yellow)})
        else:
            results.append({'item_added': item, 'message': Message('You pick up the {0}.'.format(item.name), libtcod.lighter_blue)})
            self.contents.append(item)
        return results

    def use_item(self, item_entity, **kwargs):
        results=[]
        if item_entity.item.use_function is None:
            results.append({'message': Message('You don\'t see a way to use the {0}.'.format(item_entity.name), libtcod.yellow)})
        else:
            if item_entity.item.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs={**item_entity.item.function_kwargs, **kwargs}
                item_use_results=item_entity.item.use_function(self.owner, **kwargs)
                for result in item_use_results:
                    if result.get('consumed'):
                        try:
                            self.contents.remove(item_entity)
                        except ValueError:
                            print('Cannot remove {0}'.format(item_entity))
                            print('Current inventory contents are: {0}'.format(self.contents))
                results.extend(item_use_results)
        return results

    def drop_item(self, item):
        results=[]
        item.x=self.owner.x
        item.y=self.owner.y
        self.contents.remove(item)
        results.append({'item_dropped': item, 'message': Message('You drop the {0}.'.format(item.name), libtcod.lighter_blue)})
        return results
