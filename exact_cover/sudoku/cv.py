import collections.abc

import cv2 as cv
import numpy as np
import numpy.typing as npt
import skimage.segmentation

BLUR_KERNEL_SIZE = 3
BORDER_BUFFER_SIZE = 3
THRESH_BLOCK_SIZE = 11
THRESH_C = 2

class SudokuDetector:
    def __init__(
        self,
        blur_kernel_size: int = BLUR_KERNEL_SIZE,
        border_buffer_size: int = BORDER_BUFFER_SIZE,
        thresh_block_size: int = THRESH_BLOCK_SIZE,
        thresh_C: int = THRESH_C,
    ):
        self.blur_kernel_size = blur_kernel_size
        self.border_buffer_size = border_buffer_size
        self.thresh_block_size = thresh_block_size
        self.thresh_C = thresh_C

        self.cnt_ref = np.array(
            [
                [[0, 0]],
                [[450, 0]],
                [[450, 450]],
                [[0, 450]],
            ],
        )

    def extract_board(self, img: npt.NDArray[np.uint8]) -> collections.abc.Generator[npt.NDArray[np.uint8]]:
        blurred = cv.GaussianBlur(
            img,
            (self.blur_kernel_size, self.blur_kernel_size),
            0,
        )
        threshed = cv.adaptiveThreshold(
            blurred,
            255,
            cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv.THRESH_BINARY,
            blockSize = self.thresh_block_size,
            C = self.thresh_C,
        )

        cnts, _ = cv.findContours(
            cv.bitwise_not(threshed),
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

        for cnt_it in viable_cnts:
            M = cv.getPerspectiveTransform(
                cnt_it.astype(np.float32),
                self.cnt_ref.astype(np.float32),
            )
            yield cv.warpPerspective(img, M, (450, 450))

    def extract_squares(self, img: npt.NDArray[np.uint8]) -> list[list[npt.NDArray[np.uint8]]]:
        res = [
            [
                None
                for _ in range(9)
            ]
            for _ in range(9)
        ]

        for i in range(9):
            for j in range(9):
                img_it = img[i * 50:(i + 1) * 50, j * 50:(j + 1) * 50]
                _, img_it = cv.threshold(img_it, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
                img_it = cv.bitwise_not(img_it)

                img_it_wo_border = skimage.segmentation.clear_border(
                    img_it,
                    self.border_buffer_size,
                )
                img_it_wo_border = cv.bitwise_not(img_it_wo_border)

                res[i][j] = img_it_wo_border

        return res

    def normalize_contour(self, cnt: npt.NDArray[np.int32]) -> npt.NDArray[np.int32] | None:
        try:
            cnt = cv.approxPolyN(cnt, 4)
            cnt = cnt[0, :, :].reshape((4, 1, 2))
        except:
            return None

        cnt_center = cnt.mean(axis=0).flatten()
        cnt_indices = sorted(
            range(4),
            key = lambda point_ct: np.atan2(
                *reversed(
                    (cnt[point_ct, 0, :] - cnt_center).tolist(),
                ),
            ),
        )

        return cnt[cnt_indices, :, :]
