#pylint: disable=no-member
import tcod as libtcod

class Brute:
    def take_turn(self, target, fov_map, game_map, entities):
        results=[]
        monster=self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target)>=2:
                monster.move_astar(target, entities, game_map)
            elif target.combatant.health>0:
                results.extend(monster.combatant.attack_physical(target))
        return results