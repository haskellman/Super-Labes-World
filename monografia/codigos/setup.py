def setup(self,tmx_map, dest_map, src_map): # carrega o mapa 
    self.current_map = dest_map
    for group in (self.all_sprites, self.collision_sprites, self.character_sprites, self.transition_sprites, self.dialogs_sprites, self.interaction_sprites):
        group.empty()  # clean all sprite groups
    # map theme
    self.audios[src_map].stop()
    self.audios[dest_map].play(-1)   
    try: # Terrenos
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, GAME_LAYERS['bg'])
    except ValueError as ve:
        pass
    try:  # agua
        for obj in tmx_map.get_layer_by_name('Lake'):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprite((x,y), self.overworld_frames['water'], self.all_sprites, GAME_LAYERS['water'])
    except ValueError as ve:
        pass
    try:  # objetos
        for obj in tmx_map.get_layer_by_name('Objects'):
            CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
    except ValueError as ve:
        pass
    try:  # Colisões invisíveis
        for obj in tmx_map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.collision_sprites))
    except ValueError as ve:
        pass
    try:  # transitions
        for obj in tmx_map.get_layer_by_name('Transitions'):
            # print(obj.x, obj.y, obj.properties['dest'], obj.properties['src'])
            TransitionSprite((obj.x, obj.y), obj.properties['dest'], obj.properties['src'], self.transition_sprites, (obj.width, obj.height))
    except ValueError as ve:
        pass
    try:  # entities
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                if obj.properties['pos'] == src_map:
                    self.player = Player(
                        pos = (obj.x, obj.y),
                        groups = self.all_sprites,
                        frames = self.overworld_frames['characters']['player1'],
                        facing_direction = obj.properties['direction'],
                        collision_sprites = self.collision_sprites,
                        character_data = CHARACTERS_DATA[obj.properties['character_id']],
                    )
            else:
                Character(
                    pos = (obj.x, obj.y), 
                    groups = (self.all_sprites, self.collision_sprites, self.character_sprites),
                    frames = self.overworld_frames['characters'][obj.properties['graphic']], 
                    facing_direction = obj.properties['direction'],
                    collision_sprites = self.collision_sprites,
                    character_data = CHARACTERS_DATA[obj.properties['character_id']],
                )
    except ValueError as ve:
        pass