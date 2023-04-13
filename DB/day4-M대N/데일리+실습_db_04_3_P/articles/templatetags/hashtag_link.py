from django import template
register = template.Library()

@register.filter
def hashtag_check(article):
    content = article.content
    hashtags = article.hashtag.all()

    for hashtag in hashtags:
        # #디장고 => <a href="">#디장고 </a>
        content = content.replace(
            hashtag.content, f'<a href="/articles/{hashtag.id}/hashtag">{hashtag.content}</a>'
        )
    return content