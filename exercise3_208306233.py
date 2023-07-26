#ishay eldar 208306233

import pandas as pd


class myData:
    def __init__(self, path1, path2, path3):
        """
        Initialize myData object.

        Args:
            path1 (str): Path to the books data file.
            path2 (str): Path to the rating data file.
            path3 (str): Path to the users data file.
        """
        #self.books_data = pd.read_csv(path1, sep=";", on_bad_lines='skip', encoding='latin-1')
        self.books_data = pd.read_csv(path1, sep=";", on_bad_lines='skip', encoding='latin-1',
                                      dtype={'Year-Of-Publication': str})
        self.rating_data = pd.read_csv(path2, sep=";", on_bad_lines='skip', encoding='latin-1')
        self.users_data = pd.read_csv(path3, sep=";", on_bad_lines='skip', encoding='latin-1')

        # Remove rows with non-numeric values in column 3
        self.books_data['Year-Of-Publication'] = pd.to_numeric(self.books_data['Year-Of-Publication'], errors='coerce')
        self.books_data = self.books_data.dropna(subset=['Year-Of-Publication'])

        # Convert column 3 to int32
        self.books_data['Year-Of-Publication'] = self.books_data['Year-Of-Publication'].astype('int32')
        self.rating_data = pd.read_csv(path2, sep=";", on_bad_lines='skip', encoding='latin-1')
        self.users_data = pd.read_csv(path3, sep=";", on_bad_lines='skip', encoding='latin-1')

    def num_year(self, x, y):
        """
        Calculate the number of rows in the 'Year-Of-Publication' column within the range [x, y).

        Args:
            x (int): Start year (inclusive).
            y (int): End year (exclusive).

        Returns:
            int: Number of rows within the given range.
        """
        return len(self.books_data[(self.books_data['Year-Of-Publication'] >= x) & (self.books_data['Year-Of-Publication'] < y)])

    def df_published(self, year):
        """
        Get a dataframe with the book title and author of books published in the given year.

        Args:
            year (int): Year of publication.

        Returns:
            pandas.DataFrame: Dataframe with book title and author columns.
        """
        return self.books_data.loc[self.books_data['Year-Of-Publication'] == year, ['Book-Title', 'Book-Author']]

    def num_books_by_year(self, x, y):
        """
        Get a list of tuples containing the year and the number of books published in that year.

        Args:
            x (int): Start year (inclusive).
            y (int): End year (inclusive).

        Returns:
            list: List of tuples (year, num_books).
        """
        years = range(x, y + 1)
        num_books = [(year, len(self.books_data[self.books_data['Year-Of-Publication'] == year]))
                     for year in years if len(self.books_data[self.books_data['Year-Of-Publication'] == year]) > 0]
        return num_books

    def mean_std(self, country):
        """
        Calculate the mean and standard deviation of the age of users from the given country.

        Args:
            country (str): Country name.

        Returns:
            str: A string in the format "(mean, std)" with mean and standard deviation rounded to three decimal places.
        """
        country_users = self.users_data[self.users_data['Location'].str.split(',').str[-1].str.strip().str.lower() == country.lower()]
        mean = country_users['Age'].mean()
        std = country_users['Age'].std()
        return f"({round(mean, 3)}, {round(std, 3)})"

    def find_isbn(self, book_name):
        """
        Find the ISBN(s) for the given book title.

        Args:
            book_name (str): Book title.

        Returns:
            list: List of ISBNs representing the given book.
        """
        book_isbns = self.books_data[self.books_data['Book-Title'].str.lower() == book_name.lower()]['ISBN'].tolist()
        return book_isbns

    def mean_rating(self, book_name):
        """
        Calculate the average rating for the given book.

        Args:
            book_name (str): Book title.

        Returns:
            float: Average rating for the given book.
        """
        isbn_list = self.find_isbn(book_name)
        total_rating = 0
        count = 0
        for isbn in isbn_list:
            book_ratings = self.rating_data[self.rating_data['ISBN'] == isbn]['Book-Rating']
            total_rating += book_ratings.sum()
            count += len(book_ratings)
        if count > 0:
            average_rating = total_rating / count
        else:
            average_rating = 0
        return average_rating

    def top_K(self, K):
        """
        Get a dataframe with the top K books based on ratings.

        Args:
            K (int): Number of top books to retrieve.

        Returns:
            pandas.DataFrame: Dataframe with book title, author, and rating columns.
        """
        merged_data = self.rating_data.merge(self.books_data, on='ISBN')
        book_ratings = merged_data.groupby(['Book-Title', 'Book-Author'])['Book-Rating'].mean().reset_index()
        sorted_ratings = book_ratings.sort_values(by=['Book-Rating', 'Book-Author'], ascending=[False, True]).head(K)
        return sorted_ratings[['Book-Title', 'Book-Author', 'Book-Rating']].reset_index(drop=True)

    def most_active(self, K):
        """
        Get the number of books rated by the Kth most active user.

        Args:
            K (int): Position of the user in the list of most active users.

        Returns:
            int: Number of books rated by the Kth most active user.
        """
        user_counts = self.rating_data['User-ID'].value_counts()
        sorted_users = user_counts.index.tolist()
        if K <= len(sorted_users):
            user_at_k = sorted_users[K - 1]
            return user_counts[user_at_k]
        else:
            return 0



#if __name__ == "__main__":
       # Create an instance of myData
       #md = myData('books.csv', 'ratings.csv', 'users.csv')
    # Test the num_year function
    # num_books = md.num_year(2000, 2012)
    # print(f"Number of books published between 2000 and 2010: {num_books}")

    # Test the df_published function
    # df = md.df_published(2010)
    # print(f"Books published in 2005:\n{df}")
    """
    # Test the num_books_by_year function
    books_by_year = md.num_books_by_year(2000, 2020)
    print("Number of books published by year:")
    for year, num_books in books_by_year:
        print(f"{year}: {num_books}")

    # Test the mean_std function
    country = "United States"
    mean_std = md.mean_std(country)
    print(f"Mean and standard deviation of ages for users from {country}: {mean_std}")

    # Test the find_isbn function
    book_name = "Harry Potter and the Sorcerer's Stone"
    isbns = md.find_isbn(book_name)
    print(f"ISBNs for the book '{book_name}': {isbns}")

    # Test the mean_rating function
    book_name = "The Da Vinci Code"
    average_rating = md.mean_rating(book_name)
    print(f"Average rating for the book '{book_name}': {average_rating}")

    # Test the top_K function
    K = 5
    top_books = md.top_K(K)
    print(f"Top {K} books based on ratings:")
    print(top_books)

    # Test the most_active function
    K = 3
    num_books_rated = md.most_active(K)
    print(f"Number of books rated by the {K}th most active user: {num_books_rated}")

 """

