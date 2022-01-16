class Explode(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.action = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        try:
            self.action = self.frames[self.cur_frame]
            self.cur_frame += 1
            return self.action
        except:
            pass

def load_image(name):
    image = pygame.image.load(name)
    image = image.convert_alpha()
    return image

explode = Explode(load_image("explosion.png"), 4, 8, 50, 50)
while explode.cur_frame <= len(explode.frames) - 1:
    screen.blit(explode.update(), (0, 0))
    # screen.blit(explode.update())