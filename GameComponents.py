import pygame


# square class
class Square:
    def __init__(self, screen, width, height, num):
        self.screen = screen
        self.width = width
        self.height = height
        self.num = num
        # for tile image
        self.img1 = pygame.image.load("images/stick2.png").convert_alpha()
        # for yellow image
        self.img2 = pygame.image.load("images/yellow.png").convert_alpha()
        self.img_w = 70
        self.img_h = 70
        self.sqr_img1 = pygame.transform.scale(self.img1, (self.img_w, self.img_h))
        self.sqr_img2 = pygame.transform.scale(self.img2, (self.img_w, self.img_h))

        self.sqr_lst = []

    def create_rect(self, x, y, img):
        # rectangle of sqr_img
        sqr_rect = img.get_rect()
        sqr_rect.topleft = (x, y)
        return sqr_rect

    def draw_square(self, possible_moves):
        # creating square
        sqr_lst = self.sqr_lst
        w = self.width
        h = self.height
        sqr_w = self.img_w + 2
        sqr_h = self.img_h + 2
        for i in range(self.num):
            for j in range(4):
                # we change color for possible moves
                move = 4 * i + j
                if move in possible_moves:
                    # calling rect method to create yellow rect at desire position
                    sqr = self.create_rect(w + sqr_w * j, h, self.sqr_img2)

                    self.screen.blit(self.sqr_img2, sqr)
                    sqr_lst.append(sqr)
                else:
                    # else blit cover tiles image
                    sqr = self.create_rect(w + sqr_w * j, h, self.sqr_img1)

                    self.screen.blit(self.sqr_img1, sqr)
                    sqr_lst.append(sqr)
            h = h + sqr_h
        return sqr_lst

    def show_won_lost_card(self, img, user_input):
        s_img = pygame.image.load(img).convert_alpha()
        sqr_img = pygame.transform.scale(s_img, (70, 70))
        self.screen.blit(sqr_img, self.sqr_lst[user_input].topleft)


# button class
class Button:
    def __init__(self, screen, img, widht, height):
        self.screen = screen
        self.ig = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.ig, (80, 80))
        self.w = widht
        self.h = height
        self.rect_img = self.img.get_rect()
        self.rect_img.topleft = (self.w, self.h)

    def draw(self):
        self.screen.blit(self.img, self.rect_img)

    def clicked(self):
        # button is clicked from mouse then return True
        # position
        pos = pygame.mouse.get_pos()
        if self.rect_img.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

        return False
