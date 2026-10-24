# ==========================================================
# download.py
# Download the records as a PDF or JPG file (uses Pillow).
# ==========================================================

import os
import tkinter as tk  # noqa: F401  (kept for consistency with other modules)
from datetime import datetime
from tkinter import filedialog, messagebox


class DownloadMixin:
    """Export records to PDF / JPG."""

    def load_pil_font(self, size, bold=False):
        # MAIN COMMENT: Loads a TrueType font for the exported image. Tries
        # Arial first, then DejaVu, and falls back to PIL's default font.
        from PIL import ImageFont

        if bold:
            names = ["arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"]
        else:
            names = ["arial.ttf", "Arial.ttf", "DejaVuSans.ttf"]

        for name in names:
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue

        return ImageFont.load_default()

    def render_records_pages(self, rows_per_page):
        # MAIN COMMENT: Draws the records table as one or more PIL images
        # (one image per page) and returns them as a list.
        from PIL import Image, ImageDraw

        # Page layout sizes (pixels)
        col_widths = [260, 260, 220, 130, 190, 190, 150]
        margin = 60
        table_width = sum(col_widths)
        page_width = table_width + margin * 2
        top = 190
        header_h = 70
        row_h = 64
        bottom = 90

        # Fonts
        title_font = self.load_pil_font(46, bold=True)
        sub_font = self.load_pil_font(24)
        head_font = self.load_pil_font(24, bold=True)
        cell_font = self.load_pil_font(22)

        # Split the records into pages
        rows_per_page = max(1, rows_per_page)
        chunks = [
            self.records[i:i + rows_per_page]
            for i in range(0, len(self.records), rows_per_page)
        ]
        total_pages = len(chunks)
        rows_for_height = rows_per_page if total_pages > 1 else len(chunks[0])

        def draw_centered(draw, text, box, font, fill):
            # Draws text centered inside a cell; shortens it with "…" if too wide
            x, y, w, h = box
            text = str(text)
            bbox = draw.textbbox((0, 0), text, font=font)

            while (bbox[2] - bbox[0]) > w - 20 and len(text) > 1:
                text = text[:-2] + "…" if not text.endswith("…") else text[:-2] + "…"
                bbox = draw.textbbox((0, 0), text, font=font)

            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(
                (x + (w - tw) / 2 - bbox[0], y + (h - th) / 2 - bbox[1]),
                text, font=font, fill=fill,
            )

        pages = []

        for page_no, chunk in enumerate(chunks, start=1):
            page_height = top + header_h + row_h * rows_for_height + bottom
            image = Image.new("RGB", (page_width, page_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)

            # Title + generated time
            draw.text((margin, 50), "Borrowing Records", font=title_font, fill="#123A8C")
            draw.text(
                (margin, 115),
                f"Borrowise | Generated {datetime.now().strftime('%B %d, %Y %I:%M %p')}",
                font=sub_font, fill="#6689A8",
            )

            # Heading row
            x = margin
            for name, w in zip(self.TABLE_COLUMNS, col_widths):
                draw.rectangle([x, top, x + w, top + header_h], fill="#DDF1FC", outline="#A8C5DF", width=2)
                draw_centered(draw, name, (x, top, w, header_h), head_font, "#123F87")
                x += w

            # Data rows
            for r, record in enumerate(chunk):
                y = top + header_h + r * row_h
                fill = "#FFFFFF" if r % 2 == 0 else "#F2F8FD"
                x = margin
                for key, w in zip(self.TABLE_KEYS, col_widths):
                    draw.rectangle([x, y, x + w, y + row_h], fill=fill, outline="#C8DDF2", width=2)
                    draw_centered(draw, record.get(key, ""), (x, y, w, row_h), cell_font, "#123F87")
                    x += w

            # Footer
            footer_y = top + header_h + row_h * rows_for_height + 30
            draw.text(
                (margin, footer_y),
                f"Total records: {len(self.records)} Page {page_no} of {total_pages}",
                font=sub_font, fill="#6689A8",
            )

            pages.append(image)

        return pages

    def download_records(self, file_format):
        # MAIN COMMENT: Asks where to save, then exports the records as a
        # PDF (15 rows per page) or a single long JPG image.

        # Nothing to export
        if not self.records:
            messagebox.showwarning("Borrowise", "There are no records to download yet.")
            return

        # Pillow is required for drawing the file
        try:
            import PIL  # noqa: F401
        except ImportError:
            messagebox.showerror(
                "Borrowise",
                "Downloading needs the Pillow library.\n\n"
                "Install it by running:\n pip install pillow",
            )
            return

        stamp = datetime.now().strftime("%Y%m%d_%H%M")

        # Ask the user for the file name / location
        if file_format == "pdf":
            path = filedialog.asksaveasfilename(
                parent=self.root,
                title="Download Borrowing Records (PDF)",
                defaultextension=".pdf",
                initialfile=f"Borrowise_Records_{stamp}.pdf",
                filetypes=[("PDF file", "*.pdf")],
            )
        else:
            path = filedialog.asksaveasfilename(
                parent=self.root,
                title="Download Borrowing Records (JPG)",
                defaultextension=".jpg",
                initialfile=f"Borrowise_Records_{stamp}.jpg",
                filetypes=[("JPG image", "*.jpg")],
            )

        # User pressed Cancel
        if not path:
            return

        # Draw and save the file
        try:
            if file_format == "pdf":
                if not path.lower().endswith(".pdf"):
                    path += ".pdf"
                pages = self.render_records_pages(rows_per_page=15)
                pages[0].save(
                    path, "PDF", resolution=150.0,
                    save_all=True, append_images=pages[1:],
                )
            else:
                if not path.lower().endswith((".jpg", ".jpeg")):
                    path += ".jpg"
                page = self.render_records_pages(rows_per_page=len(self.records))[0]
                page.save(path, "JPEG", quality=95)
        except Exception as error:
            messagebox.showerror("Borrowise", f"Could not save the file.\n\n{error}")
            return

        messagebox.showinfo(
            "Borrowise", f"Records downloaded successfully!\n\n{os.path.basename(path)}"
        )
