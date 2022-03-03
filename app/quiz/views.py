from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPUnauthorized, HTTPBadRequest
from aiohttp_apispec import querystring_schema, request_schema, response_schema
from app.quiz.models import Answer
from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin):
    @request_schema(ThemeSchema)
    async def post(self):
        await self.auth()
        title = self.data["title"]
     
        for stored_theme in self.request.app.database.themes:
            if title == stored_theme.title:
                raise HTTPConflict
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin):
    @response_schema(ThemeSchema)
    async def get(self):
        await self.auth()
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))

class QuestionAddView(AuthRequiredMixin):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        await self.auth()
        title = self.data["title"]
        theme_id = self.data["theme_id"]
        answers = self.data["answers"]

        if len(answers) < 2:
            raise HTTPBadRequest

        if await self.store.quizzes.get_question_by_title(title) is not None:
            raise HTTPConflict

        if await self.store.quizzes.get_theme_by_id(theme_id) is None:
            raise HTTPNotFound
        parsed_answers = []
        correct = []
        for answer in self.data["answers"]:
            answer = Answer(title=answer["title"], is_correct=answer["is_correct"])
            if answer.is_correct and True in correct:
                raise HTTPBadRequest
            correct.append(answer.is_correct)
            parsed_answers.append(answer)

        if not any(correct):
            raise HTTPBadRequest
        question = await self.store.quizzes.create_question(title=title, theme_id=theme_id, answers=answers)
        return json_response(data=QuestionSchema().dump(question))
        


class QuestionListView(AuthRequiredMixin):  
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        await self.auth()
        questions = await self.store.quizzes.list_questions(theme_id=self.data.get("theme_id"))
        return json_response(data=ListQuestionSchema().dump({"questions": questions}))
