from dash_slides import presentation
from dash_slides.presentation import Presentation, PresentationApp
from dash_slides.slides import FlowSlide, ImageSlide, ListSlide, MarkdownSlide, SplitSlide, TitleSlide

presentation = Presentation()
presentation.add_slide(TitleSlide(title="Feedback on RIRAG", 
                                  subtitle="Regulatory information retrieval and answer generation shared task", 
                                  authors=["Ismaël Rousseau"]))
presentation.add_slide(ImageSlide(img_path="assets/imgs/regnlp.png"))
presentation.add_slide(SplitSlide(TitleSlide("Outline"), 
                                  ListSlide(items=["Presentation of the Shared Task", "Proposed methodology", "What didn't work"]),
                                  mode="column"))
presentation.add_slide(SplitSlide(first_slide=TitleSlide(title="ObliQA Dataset"), second_slide=ImageSlide(img_path="assets/imgs/ObliQA.png"), mode="column"))

obliqa_example = """```json
    {
        "QuestionID": "777e7a14-fea3-4c37-a0e6-9ffb50024d5c",
        "Question": "Can the ADGM provide clarity on the level of detail and documentation that should accompany a report of suspicious activity to ensure it meets regulatory standards?",
        "Passages": [
            {
                "DocumentID": 1,
                "PassageID": "14.2.3.Guidance.10.",
                "Passage": "Relevant Persons should comply with guidance issued by the EOCN with regard to identifying and reporting suspicious activity and Transactions relating to money laundering, terrorist financing and proliferation financing."
            }
        ],
        "Group": 2
    },
    {
        "QuestionID": "0eb99ea8-3810-492c-9986-7739006b5708",
        "Question": "Are there any exceptions or specific circumstances under which the real-time reporting requirements for Virtual Asset transactions may be waived or modified?",
        "Passages": [
            {
                "DocumentID": 19,
                "PassageID": "100)",
                "Passage": "REGULATORY REQUIREMENTS FOR AUTHORISED PERSONS ENGAGED IN REGULATED ACTIVITIES IN RELATION TO VIRTUAL ASSETS\nMarket Abuse, Transaction Reporting and Misleading Impressions (FSMR)\nSimilar to the reporting requirements imposed on Recognised Investment Exchanges and MTFs in relation to Financial Instruments, MTFs (pursuant to FSMR Section 149) are required to report details of transactions in Accepted Virtual Assets traded on their platforms.   The FSRA expects MTFs using Virtual Assets to report to the FSRA on both a real-time and batch basis.\n"
            }
        ],
        "Group": 2
    }
```"""

table = """| Scorer | R@10&nbsp;&nbsp; | M@10 |
| --- | --- | --- |
| BM-25 | 0.59 | x |
| Simbow | 0.58 | x |
| MiniLM-L6-V2 | 0.63 | x |
| StellaEN (s2p)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 0.70&nbsp;&nbsp;&nbsp; | x |
| StellaEN (s2s) | 0.71 | x |
"""
presentation.add_slide(MarkdownSlide(obliqa_example, footer="An example of ObliQA data"))
presentation.add_slide(MarkdownSlide(table, footer="An example of ObliQA data"))
presentation_app = PresentationApp(presentation)
presentation_app.start()