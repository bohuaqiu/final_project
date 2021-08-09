import math


class SingleAttack():#普通攻擊（次氯酸水）的攻擊方式
    def attack(self, enemies, bullet):
        for en in enemies.get():#逐個搜索場上的病毒
            if en.is_hitted(bullet.rect.center):
                en.get_hurt(bullet.dmg)#擊中病毒后對其造成傷害
                bullet.bullet_del=True#擊中病毒後將子彈移除
                break


class AOE():
    def attack(self, enemies, bullet):#酒精的攻擊方式
        for en in enemies.get():
            '''
            因為是範圍攻擊所以會判斷病毒是否進入子彈的有效範圍，並且不對“不可攻擊”的病毒進行攻擊以避免同一發子彈對病毒造成多次傷害
            '''
            if (bullet.rect.collidepoint(en.rect.center) and en.pass_dmg==False):
                en.get_hurt(bullet.dmg)
                en.rect.centerx+=bullet.del_x#酒精帶有擊退效果，會根據子彈的向量數據擊退病毒
                en.rect.centery+=bullet.del_y
