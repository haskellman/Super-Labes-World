def draw_rectangles(self):
    # rectangles
    rect_A = pygame.Rect(632, 540, self.rect_width, self.rect_height)
    rect_B = pygame.Rect(942, 540, self.rect_width, self.rect_height)
    rect_C = pygame.Rect(632, 630, self.rect_width, self.rect_height)
    rect_D = pygame.Rect(942, 630, self.rect_width, self.rect_height)
    # icon
    self.icon = self.interface_frames['interface'][str(self.option)]
    # draw
    if self.option == 0:
        self.display_surface.blit(self.icon, rect_A, special_flags = pygame.BLEND_RGB_ADD )
    elif self.option == 1:
        self.display_surface.blit(self.icon, rect_B, special_flags = pygame.BLEND_RGB_ADD )
    elif self.option == 2:
        self.display_surface.blit(self.icon, rect_C, special_flags = pygame.BLEND_RGB_ADD )
    elif self.option == 3:
        self.display_surface.blit(self.icon, rect_D, special_flags = pygame.BLEND_RGB_ADD )