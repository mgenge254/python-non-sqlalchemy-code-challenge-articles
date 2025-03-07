class Article:
    all = []  # Class variable to track all articles

    def __init__(self, author, magazine, title):
        if not isinstance(title, str):
            raise ValueError("Title must be a string, e.g., 'How to Code'")
        if not (5 <= len(title) <= 50):
            raise ValueError("Title must be 5-50 characters, e.g., 'Python Basics'")
        if not isinstance(author, Author):
            raise TypeError("Author must be an Author instance, e.g., Author('John Doe')")
        if not isinstance(magazine, Magazine):
            raise TypeError("Magazine must be a Magazine instance, e.g., Magazine('Tech Today', 'Tech')")
        
        self._title = title  # Immutable
        self.author = author  # Using setter for mutability
        self.magazine = magazine  # Using setter for mutability
        self.author._articles.append(self)  # Track relationship
        self.magazine._articles.append(self)  # Track relationship
        Article.all.append(self)  # Track all instances

    @property
    def title(self):
        return self._title  # No setter - immutable

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise TypeError("Author must be an Author instance, e.g., Author('Jane Smith')")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise TypeError("Magazine must be a Magazine instance, e.g., Magazine('Vogue', 'Fashion')")
        self._magazine = value


class Author:
    def __init__(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string, e.g., 'Carry Bradshaw'")
        if len(name) <= 0:
            raise ValueError("Name must be non-empty, e.g., 'John'")
        self._name = name  # Immutable
        self._articles = []  # To track articles

    @property
    def name(self):
        return self._name  # No setter - immutable

    def articles(self):
        return self._articles  # List of Article instances

    def magazines(self):
        return list(set(article.magazine for article in self._articles))  # Unique Magazine instances

    def add_article(self, magazine, title):
        return Article(self, magazine, title)  # Creates and returns new Article

    def topic_areas(self):
        if not self._articles:
            return None
        return list(set(magazine.category for magazine in self.magazines()))  # Unique categories


class Magazine:
    def __init__(self, name, category):
        self.name = name  # Using setter
        self.category = category  # Using setter
        self._articles = []  # To track articles

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string, e.g., 'Vogue'")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be 2-16 characters, e.g., 'Tech Weekly'")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Category must be a string, e.g., 'Fashion'")
        if len(value) <= 0:
            raise ValueError("Category must be non-empty, e.g., 'Technology'")
        self._category = value

    def articles(self):
        return self._articles  # List of Article instances

    def contributors(self):
        return list(set(article.author for article in self._articles))  # Unique Author instances

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self._articles]  # List of title strings

    def contributing_authors(self):
        if not self._articles:
            return None
        author_counts = {}
        for article in self._articles:
            author_counts[article.author] = author_counts.get(article.author, 0) + 1
        result = [author for author, count in author_counts.items() if count > 2]
        return result if result else None  # List of Authors with >2 articles or None


# Test code to verify functionality
if __name__ == "__main__":
    try:
        # Create instances
        author1 = Author("Carry Bradshaw")
        author2 = Author("Nathaniel Hawthorne")
        mag1 = Magazine("Vogue", "Fashion")
        mag2 = Magazine("Tech Today", "Technology")

        # Add articles
        article1 = author1.add_article(mag1, "How to Wear a Tutu with Style")
        article2 = author1.add_article(mag1, "Dating Life in NYC")
        article3 = author1.add_article(mag1, "How to Be Single and Happy")
        article4 = author2.add_article(mag2, "2023 Tech Trends Unveiled")

        # Verify functionality
        print(f"All articles: {len(Article.all)}")  # Should be 4
        print(f"{author1.name}'s articles: {[a.title for a in author1.articles()]}")
        print(f"{mag1.name}'s titles: {mag1.article_titles()}")
        print(f"{mag1.name}'s contributing authors: "
              f"{[a.name for a in mag1.contributing_authors()] if mag1.contributing_authors() else 'None'}")

        # Test immutability
        try:
            article1.title = "New Title"
        except AttributeError:
            print("Success: Title is immutable")

        try:
            author1.name = "New Name"
        except AttributeError:
            print("Success: Author name is immutable")

        # Test validation
        try:
            mag1.name = 2
        except TypeError:
            print("Success: Magazine name must be string")

        try:
            mag1.name = "New Yorker Plus X"
        except ValueError:
            print("Success: Magazine name must be 2-16 chars")

        try:
            mag1.category = 2
        except TypeError:
            print("Success: Category must be string")

        try:
            mag1.category = ""
        except ValueError:
            print("Success: Category must be non-empty")

    except Exception as e:
        print(f"Error: {e}")