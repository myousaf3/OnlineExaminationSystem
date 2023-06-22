from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from exam.models import Exam, Question, Subject
from exam.forms import QuestionForm, TextForm
from datetime import datetime, timedelta


class TextBasedViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("text-based")
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        subject = Subject.objects.create(name="Math")  # Create a Subject instance

        start_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now() + timedelta(hours=1)

        self.exam = Exam.objects.create(
            subject=subject,
            teacher=self.user,
            start_time=start_time,
            end_time=end_time
        )
        self.client.force_login(self.user)

    def test_text_based_view_with_authenticated_teacher(self):
        self.client.login(username="testuser", password="testpassword")  # Authenticate the user
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "text-based.html")
        self.assertIsInstance(response.context["question_form"], QuestionForm)
        self.assertIsInstance(response.context["text_form"], TextForm)

    def test_text_based_view_post_valid_data(self):
        data = {
            "exam": self.exam.id,
            "question_text": "Write a short essay on the importance of education.",
            "question_type": "text_based",
            "text": "Education plays a crucial role in personal and societal development.",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse("text-based"))  # Check redirection

        # Check if the question and text are created
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Text.objects.count(), 1)
        question = Question.objects.first()
        text = Text.objects.first()
        self.assertEqual(question.exam, self.exam)
        self.assertEqual(question.question_text, "Write a short essay on the importance of education.")
        self.assertEqual(question.question_type, "text_based")
        self.assertEqual(text.question, question)
        self.assertEqual(text.text, "Education plays a crucial role in personal and societal development.")

    # def test_text_based_view_post_exam_request(self):
    #     Exam.objects.create(subject="English", teacher=self.user, is_requested=True)
    #     data = {"request-btn": "", "exam_id": self.exam.id}
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, 302)  # Redirect status code
    #     self.assertRedirects(response, reverse("text-based"))  # Check redirection
    #     self.assertContains(response, "Exam request already exists.")

    # def test_text_based_view_post_nonexistent_exam(self):
    #     data = {
    #         "exam": 9999,  # Nonexistent exam ID
    #         "question_text": "Write a short essay on the importance of education.",
    #         "question_type": "text_based",
    #         "text": "Education plays a crucial role in personal and societal development.",
    #     }
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, 404)  # Check 404 status code
    #     self.assertContains(response, "Exam does not exist.")

    # def test_text_based_view_post_error(self):
    #     data = {"exam": self.exam.id, "question_text": "Write a short essay on the importance of education."}
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, 200)  # Check if the view returns to the same page
    #     self.assertContains(response, "An error occurred. Please try again later.")
