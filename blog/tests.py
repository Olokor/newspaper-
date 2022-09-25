# from turtle import title
from urllib import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post
# Create your tests here.
class Blogtest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'olokor',
            email='olokorwisdom15@gmail.com',
            password='12345'
            )
        
        self.post = Post.objects.create(
            title ='a good title',
            body = 'a good body',
            author = self.user
            
            )
    def test_string_representation(self):
        self.assertEqual(f'{self.post.title}','a good title')
        self.assertEqual(f'{self.post.author}', 'olokor') 
        self.assertEqual(f'{self.post.body}', 'a good body')
    
    def test_post_listview(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'a good body')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_post_detailview(self):
       response=self.client.get('/post/1/')
       no_response = self.client.get('/post/10000/')
       self.assertEqual(response.status_code, 200)
       self.assertEqual(no_response.status_code, 404)
       self.assertContains(response, 'a good title')
       self.assertTemplateUsed(response, 'post_detail.html')


    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'a good title')
        self.assertEqual(f'{self.post.body}', 'a good body')
        self.assertEqual(f'{self.post.author}', 'olokor')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'),{
            'title' : 'New title',
            'body': 'New Text',
            'author' : self.user.id

        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'New title')
        self.assertEqual(Post.objects.last().body, 'New Text')
        # self.assertEqual()

    def test_post_update_view(self): # new
        response = self.client.post(reverse('post_edit', args='1'), {
        'title': 'Updated title',
        'body': 'Updated text',
        })
        self.assertEqual(response.status_code, 302)
    def test_post_delete_view(self): # new
        response = self.client.post(
        reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)