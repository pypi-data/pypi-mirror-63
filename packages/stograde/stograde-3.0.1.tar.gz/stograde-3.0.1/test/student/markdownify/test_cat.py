from stograde.student.markdownify.cat import cat


def test_cat(fs):
    filename = 'foo.txt'
    contents = 'insert a story here'
    fs.create_file(filename, contents=contents)

    result = cat(filename)
    assert result[0] == 'success'
    assert result[1] == contents


def test_cat_missing(fs):
    result = cat('file.txt')
    assert result[0] == 'failure'
    assert result[1] is None
