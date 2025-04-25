from django.db import models

# Create your models here.
class Blog(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_body = models.TextField()
    blog_image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.blog_title
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment on {self.blog.blog_title}"
    

