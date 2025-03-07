import pytest

from classes.many_to_many import Author, Magazine, Article  # Adjust import path as needed


class TestAuthor:
    """Author in many_to_many.py"""

    def test_has_name(self):
        """Author is initialized with a name"""
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")

        assert author_1.name == "Carry Bradshaw"
        assert author_2.name == "Nathaniel Hawthorne"

    def test_name_is_immutable_string(self):
        """author name is of type str and cannot change"""
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")
        
        assert isinstance(author_1.name, str)
        assert isinstance(author_2.name, str)
        
        # Test immutability by expecting AttributeError
        with pytest.raises(AttributeError):
            author_1.name = "ActuallyTopher"

        # Test type validation (non-string)
        with pytest.raises(ValueError):
            Author(123)

    def test_name_has_length(self):
        """author name is longer than 0 characters"""
        author_1 = Author("Carry Bradshaw")
        
        assert len(author_1.name) > 0
        
        # Test empty string validation
        with pytest.raises(ValueError):
            Author("")

    def test_has_many_articles(self):
        """author has many articles"""
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")
        magazine = Magazine("Vogue", "Fashion")
        article_1 = Article(author_1, magazine, "How to wear a tutu with style")
        article_2 = Article(author_1, magazine, "Dating life in NYC")
        article_3 = Article(author_2, magazine, "How to be single and happy")

        assert len(author_1.articles()) == 2
        assert len(author_2.articles()) == 1
        assert article_1 in author_1.articles()
        assert article_2 in author_1.articles()
        assert article_3 in author_2.articles()

    def test_articles_of_type_articles(self):
        """author articles are of type Article"""
        author_1 = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author_1, magazine, "How to wear a tutu with style")
        Article(author_1, magazine, "Dating life in NYC")
        
        assert all(isinstance(article, Article) for article in author_1.articles())

    def test_has_many_magazines(self):
        """author has many magazines"""
        author_1 = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_1, magazine_2, "2023 Eccentric Design Trends")

        assert magazine_1 in author_1.magazines()
        assert magazine_2 in author_1.magazines()
        assert len(author_1.magazines()) == 2

    def test_magazines_of_type_magazine(self):
        """author magazines are of type Magazine"""
        author_1 = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_1, magazine_2, "2023 Eccentric Design Trends")

        assert all(isinstance(magazine, Magazine) for magazine in author_1.magazines())

    def test_magazines_are_unique(self):
        """author magazines are unique"""
        author_1 = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_1, magazine_2, "2023 Eccentric Design Trends")
        Article(author_1, magazine_2, "Carrara Marble is so 2020")

        assert len(author_1.magazines()) == 2  # Still only 2 unique magazines

    def test_add_article(self):
        """creates and returns a new article given a magazine and title"""
        author_1 = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        article = author_1.add_article(magazine, "How to wear a tutu with style")

        assert isinstance(article, Article)
        assert article.author == author_1
        assert article.magazine == magazine
        assert article.title == "How to wear a tutu with style"
        assert article in author_1.articles()

    def test_topic_areas(self):
        """returns a list of topic areas for all articles by author"""
        author_1 = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_1, magazine_2, "2023 Eccentric Design Trends")

        topics = author_1.topic_areas()
        assert "Fashion" in topics
        assert "Architecture" in topics
        assert len(topics) == 2

        # Test no articles case
        author_2 = Author("Nathaniel Hawthorne")
        assert author_2.topic_areas() is None

    def test_topic_areas_are_unique(self):
        """topic areas are unique"""
        author_1 = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        magazine_3 = Magazine("Trendy", "Fashion")  # Same category as Vogue
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_1, magazine_2, "2023 Eccentric Design Trends")
        Article(author_1, magazine_3, "Dating life in NYC")

        topics = author_1.topic_areas()
        assert len(topics) == 2  # Only 2 unique categories: Fashion, Architecture
        assert "Fashion" in topics
        assert "Architecture" in topics