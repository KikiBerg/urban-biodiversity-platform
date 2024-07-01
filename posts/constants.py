"""
This module defines constants used throughout the posts app.
"""

################################## Status choices for blog posts
STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
]

"""
Choices for the status of a blog post.

Possible values:
- 'draft': The post is a draft and not published yet.
- 'published': The post is published and visible to users.
"""


################################## Status choices for comments
COMMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

"""
Choices for the status of a comment.

Possible values:
- 'pending': The comment is pending review and not visible to users.
- 'approved': The comment is approved and visible to users.
- 'rejected': The comment is rejected and not visible to users.
"""


################################## Status choices for categories
STATUS_CATEGORIES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

