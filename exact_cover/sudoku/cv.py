import cv2 as cv
import cv2.typing as cvt
import numpy as np
import numpy.typing as npt

THRESH_BLOCK_SIZE = 11
THRESH_C = 2

class SudokuDetector:
    def __init__(
        self,
        thresh_block_size: int = THRESH_BLOCK_SIZE,
        thresh_C: int = THRESH_C,
    ):
        self.thresh_block_size = thresh_block_size
        self.thresh_C = thresh_C

    def apply_blur(self, img: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        return img

    def apply_threshold(self, img: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        res = cv.adaptiveThreshold(
            img,
            255,
            cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv.THRESH_BINARY,
            blockSize = self.thresh_block_size,
            C = self.thresh_C,
        )
        return res

    def extract_squares(self, img: npt.NDArray[np.uint8]) -> list[np.uint8]:
        cnts, _ = cv.findContours(
            img,
            cv.RETR_LIST,
            cv.CHAIN_APPROX_SIMPLE,
        )
        normalized_cnts = [
            self.normalize_contour(cnt_it)
            for cnt_it in cnts
        ]
        viable_cnts = sorted(
            (
                cnt_it
                for cnt_it in normalized_cnts
                if cnt_it is not None
            ),
            key = cv.contourArea,
            reverse = True,
        )

        M = cv.getPerspectiveTransform(
            np.array([e[0] for e in viable_cnts[0]], dtype=np.float32),
            np.array([[0, 0], [450, 0], [450, 450], [0, 450]], dtype=np.float32),
        )
        return cv.warpPerspective(img, M, (450, 450))

    def normalize_contour(self, cnt: cvt.MatLike) -> cvt.MatLike | None:
        if cnt.shape != (4, 1, 2):
            return None

        if not cv.isContourConvex(cnt):
            return None

        no_points = cnt.shape[0]
        cnt_center = cnt.mean(axis=0).flatten()

        cnt_indices = sorted(
            range(no_points),
            key = lambda point_ct: np.atan2(
                *reversed(
                    (cnt[point_ct, 0, :] - cnt_center).tolist(),
                ),
            ),
        )

        return cnt[cnt_indices, :, :]
