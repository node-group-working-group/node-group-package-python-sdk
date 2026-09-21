class Metadata:
    def __init__(
        self,
        title,
        subject,
        contributors,
        publisher,
        description,
        date,
        identifier,
        language,
        license,
        version,
    ):
        self.title = title
        self.subject = subject
        self.contributors = contributors
        self.publisher = publisher
        self.description = description
        self.date = date
        self.identifier = identifier
        self.language = language
        self.license = license
        self.version = version


class Contributor:
    def __init__(self, name, contribution):
        self.name = name
        self.contribution = contribution
