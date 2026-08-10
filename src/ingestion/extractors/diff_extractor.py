"""
diff_extractor.py

Extracts raw code diffs from a GitHub Pull Request.
"""


class DiffExtractor:

    @staticmethod
    def extract(pr):

        patches = []

        for file in pr.get_files():

            if file.patch:

                patches.append(
                    f"\n### FILE: {file.filename}\n"
                    f"{file.patch}"
                )

        return "\n".join(patches)