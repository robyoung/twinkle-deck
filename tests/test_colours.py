from twinkledeck.colours import rgb_to_hsv
import pytest


@pytest.mark.parametrize(
    ("rgb", "hsv"),
    [
        # black and white
        pytest.param((0, 0, 0), (0, 0, 0), id="black"),
        pytest.param((255, 255, 255), (0, 0, 1), id="white"),
        # RGB
        pytest.param((255, 0, 0), (0, 1, 1), id="bright-red"),
        pytest.param((0, 255, 0), (1 / 3, 1, 1), id="bright-green"),
        pytest.param((0, 0, 255), (2 / 3, 1, 1), id="bright-blue"),
        pytest.param((85, 0, 0), (0, 1, 1 / 3), id="dim-red"),
        pytest.param((0, 85, 0), (1 / 3, 1, 1 / 3), id="dim-green"),
        pytest.param((0, 0, 85), (2 / 3, 1, 1 / 3), id="dim-blue"),
        pytest.param((255, 85, 85), (0, 2 / 3, 1), id="pale-red"),
        pytest.param((85, 255, 85), (1 / 3, 2 / 3, 1), id="pale-green"),
        pytest.param((85, 85, 255), (2 / 3, 2 / 3, 1), id="pale-blue"),
        # split hues
        pytest.param((0, 255, 255), (3 / 6, 1, 1), id="bright-cyan"),
        pytest.param((255, 0, 255), (5 / 6, 1, 1), id="bright-purple"),
        pytest.param((255, 255, 0), (1 / 6, 1, 1), id="bright-yellow"),
    ],
)
def test_rgb_to_hsv(rgb, hsv):
    assert_almost_equal(rgb_to_hsv(*rgb), hsv)


def assert_almost_equal(left, right):
    assert tuple(round(n, 3) for n in left) == tuple(round(n, 3) for n in right)
