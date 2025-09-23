import collections.abc

import cv2 as cv
import numpy as np
import numpy.typing as npt
import skimage.segmentation

BLUR_KERNEL_SIZE = 3
BORDER_BUFFER_SIZE = 3
NO_POINTS_PER_SEGMENT = 50
THRESH_BLOCK_SIZE = 11
THRESH_C = 2

class SudokuDetector:
    def __init__(
        self,
        blur_kernel_size: int = BLUR_KERNEL_SIZE,
        border_buffer_size: int = BORDER_BUFFER_SIZE,
        no_points_per_segment: int = NO_POINTS_PER_SEGMENT,
        thresh_block_size: int = THRESH_BLOCK_SIZE,
        thresh_C: int = THRESH_C,
    ):
        self.blur_kernel_size = blur_kernel_size
        self.border_buffer_size = border_buffer_size
        self.no_points_per_segment = no_points_per_segment
        self.thresh_block_size = thresh_block_size
        self.thresh_C = thresh_C

        self.no_points_per_side = 9 * no_points_per_segment
        self.cnt_ref = np.array(
            [
                [[0, 0]],
                [[self.no_points_per_side, 0]],
                [[self.no_points_per_side, self.no_points_per_side]],
                [[0, self.no_points_per_side]],
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
            cv.THRESH_BINARY_INV,
            blockSize = self.thresh_block_size,
            C = self.thresh_C,
        )

        cnts, _ = cv.findContours(
            threshed,
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
            yield cv.warpPerspective(img, M, (self.no_points_per_side, self.no_points_per_side))

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
                i_0 = i * self.no_points_per_segment
                i_1 = (i + 1) * self.no_points_per_segment
                j_0 = j * self.no_points_per_segment
                j_1 = (j + 1) * self.no_points_per_segment
                img_it = img[i_0:i_1, j_0:j_1]

                _, img_it_w_border = cv.threshold(
                    img_it,
                    0,
                    255,
                    cv.THRESH_BINARY_INV | cv.THRESH_OTSU,
                )
                img_it_wo_border = skimage.segmentation.clear_border(
                    img_it_w_border,
                    self.border_buffer_size,
                )

                res[i][j] = self.apply_mask(img_it, mask=img_it_wo_border)

        return res

    def extract_symbol(self, img: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        cnts, _ = cv.findContours(
            cv.bitwise_not(img),
            cv.RETR_EXTERNAL,
            cv.CHAIN_APPROX_SIMPLE,
        )
        if len(cnts) == 0:
            return img

        cnt = max(
            cnts,
            key = cv.contourArea,
        )
        #cnt = cv.approxPolyDP(cnt, 0.05, True)

        mask = np.zeros(img.shape, dtype=np.uint8)
        cv.drawContours(mask, [cnt], 0, 255, cv.FILLED)

        res = self.apply_mask(img, mask=mask)
        res = self.increase_contrast(res)

        #res = cv.dilate(
        #    res,
        #    cv.getStructuringElement(cv.MORPH_RECT, (3, 3)),
        #)

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

    def apply_mask(
        self,
        img: npt.NDArray[np.int32],
        mask: npt.NDArray[np.int32],
    ) -> npt.NDArray[np.int32]:
        img_inv = cv.bitwise_not(img)
        res = cv.bitwise_and(
            img_inv,
            img_inv,
            mask = mask,
        )
        res = cv.bitwise_not(res)

        return res

    def increase_contrast(
        self,
        img: npt.NDArray[np.int32],
        fac: float | None = None,
    ) -> npt.NDArray[np.int32]:
        img_inv = cv.bitwise_not(img)
        fac = fac or 255 / img_inv.max()

        res = cv.convertScaleAbs(img_inv, alpha=fac)
        res = cv.bitwise_not(res)

        return res
