import main
import pytest
import pyglet

def test_image_load():
    img_a = main.preload('ship1.png')
    img_b =pyglet.image.load('./res/ship1.png')
    assert img_a.width == img_b.width and img_a.height == img_b.height


def test_label_load():
    obj = main.GameWindow()
    assert obj.intro_text.italic and obj.intro_text.bold
    assert obj.enemies_destroyed.italic and obj.enemies_destroyed.bold and obj.enemies_destroyed.font_size == 16
    assert obj.score_text.italic and obj.score_text.bold and obj.score_text.font_size == 16
    assert obj.player_health.italic and obj.player_health.bold and obj.player_health.font_size == 16
    assert obj.high_score_text.italic and obj.high_score_text.bold and obj.high_score_text.font_size == 20
    assert obj.high_score_value.color == (120, 200, 150, 255)
    assert  obj.num_enemies_destroyed.color == (80, 200, 200, 255)
    assert obj.num_score.color == (200, 120, 150, 255)


def test_basic_load():
    obj = main.GameWindow()
    assert obj.player_speed == 300 and obj.player_fire_rate == 0
    assert obj.enemy_fire_rate == 0
    assert obj.enemy_typeA_spawner == 0 and obj.enemy_typeB_spawner == 0 and obj.enemy_typeA_counter == 5 and obj.enemy_typeB_counter == 10