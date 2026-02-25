from fpdf import FPDF
import os
from datetime import datetime


class StoryPDF(FPDF):
    """Custom PDF class for story export"""

    def header(self):
        """Page header"""
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(75, 0, 130)  # Purple color
        self.cell(0, 10, "Interactive Narrative Engine", align="C")
        self.ln(5)
        self.set_draw_color(75, 0, 130)
        self.line(10, 25, 200, 25)
        self.ln(10)

    def footer(self):
        """Page footer"""
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def export_story_pdf(story_data: dict) -> str:
    """
    Export a complete story to PDF file.

    Args:
        story_data: Dictionary containing story details and scenes

    Returns:
        str: Path to the generated PDF file
    """
    try:
        pdf = StoryPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # ---- Story Title ----
        pdf.set_font("Helvetica", "B", 24)
        pdf.set_text_color(75, 0, 130)
        title = f"A {story_data.get('genre', 'Fantasy').title()} Story"
        pdf.cell(0, 15, title, align="C")
        pdf.ln(5)

        # ---- Story Details ----
        pdf.set_font("Helvetica", "I", 11)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 8, f"Protagonist: {story_data.get('protagonist', 'Hero')}", align="C")
        pdf.ln(5)
        pdf.cell(0, 8, f"Generated on: {datetime.now().strftime('%B %d, %Y')}", align="C")
        pdf.ln(10)

        # ---- Divider ----
        pdf.set_draw_color(75, 0, 130)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(10)

        # ---- Story Scenes ----
        scenes = story_data.get("scenes", [])

        for i, scene in enumerate(scenes):
            # Chapter heading
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(75, 0, 130)
            pdf.cell(0, 10, f"Chapter {i + 1}", ln=True)
            pdf.ln(2)

            # Scene text
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 7, scene.get("scene_text", ""))
            pdf.ln(5)

            # User choice made
            if scene.get("user_choice") and i < len(scenes) - 1:
                pdf.set_font("Helvetica", "I", 10)
                pdf.set_text_color(100, 100, 100)
                pdf.set_fill_color(240, 240, 255)
                pdf.multi_cell(
                    0, 8,
                    f"  You chose: {scene['user_choice']}  ",
                    fill=True
                )
                pdf.ln(5)

            # Divider between chapters
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(8)

        # ---- The End ----
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(75, 0, 130)
        pdf.cell(0, 10, "~ The End ~", align="C")

        # ---- Save PDF ----
        os.makedirs("exports", exist_ok=True)
        session_id = story_data.get("session_id", "story")
        filename = f"exports/story_{session_id}.pdf"
        pdf.output(filename)

        print(f"✅ PDF exported successfully: {filename}")
        return filename

    except Exception as e:
        print(f"❌ PDF export failed: {e}")
        raise e