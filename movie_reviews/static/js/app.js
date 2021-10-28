$('#createFolderModal').on('shown.bs.modal', function () {
    $('#folderName').trigger('focus')
  });

  function createFolderFunc() {
    $.ajax({
      url: 'bookmarks/create-folder/',
      type: 'POST',
      data: $("#createFolder").serialize(),
      dataType: 'json',
      success: (data) => {
        $("#createFolderModal").modal('hide');
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  function createBookmark(event, index) {
    let folderId = $(event.target).attr("value");
    let bookmarkForm = $(event.target).parent().parent().parent();
    $(bookmarkForm).append('<input name="folder_id" type="text" value="'+ folderId +'" hidden />')
    let currIndex = index;
    if(!currIndex) {
      currIndex = $(event.target).parent()[0].id.replace('folderDropdown', '');
    } 

    $.ajax({
      url: 'bookmarks/create-bookmark/',
      type: 'POST',
      data: $(bookmarkForm).serialize(),
      headers: {
        'X-CSRFToken': '{{csrf_token}}'
      },
      dataType: 'json',
      context: this,
      success: (data) => {
        let bookmark = JSON.parse(data.bookmark);
        let parent = $('#dropdownDiv'+currIndex);
        $(parent).empty();
        $(parent).append($('<button>', {
          class:'btn btn-danger mt-4',
          type:'button',
          id:'removeButton'+currIndex,
          html: 'Remove Bookmark <i class="bi bi-lg bi-bookmark-x"></i>'
        }));
        $(parent).children().last().on('click', deleteBookmark);
        let form = $('#bookmarkForm'+currIndex);
        $(parent).append($('<input>', {
          hidden: true,
          name:'bookmarkId',
          value: bookmark[0].pk,
          id:'removeButton'+currIndex,
          html: 'Remove Bookmark <i class="bi bi-lg bi-bookmark-x"></i>'
        }));
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  function deleteBookmark(event, index) {
    let currIndex = index;
    if(!currIndex) {
      if($(event)[0].id) {
        currIndex = $(event)[0].id.replace('removeButton', '');
      } else if($(event.target)[0].id) {
        currIndex = $(event.target)[0].id.replace('removeButton', '');
      }
    }

    let bookmarkForm = $('#bookmarkForm'+currIndex);

    $.ajax({
      url: 'bookmarks/delete-bookmark/',
      type: 'POST',
      data: $(bookmarkForm).serialize(),
      dataType: 'json',
      context: this,
      success: (data) => {
        let parent = $('#dropdownDiv'+currIndex);
        $(parent).empty();
        $(parent).append($('<button>', {
          class:'btn btn-primary mt-4 dropdown-toggle',
          type:'button',
          id:'dropdownMenuButton'+currIndex,
          'data-bs-toggle':'dropdown',
          'aria-haspopup':'true',
          'aria-expanded':'false',
          html: 'Bookmark <i class="bi bi-lg bi-bookmark-plus"></i>'
        }));
        $(parent).children().last().on('click', {index:currIndex}, createBookmark);
        $(parent).append($('<div>', {
          class:'dropdown-menu',
          id:'folderDropdown'+currIndex,
          'aria-labelledby':'folderDropdownButton'
        }));
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  function getFolders(event, index) {
    $.ajax({
      url: 'bookmarks/get-folders/',
      type: 'GET',
      headers: {
        'X-CSRFToken': '{{csrf_token}}'
      },
      success: (data) => {
        $('#folderDropdown'+index).empty();
        let child;
        for(let i = 0; i < data.length; i++) {
          child = $('#folderDropdown'+index).append($('<a>', {
            value: data[i].pk,
            class: 'dropdown-item',
            text: data[i].fields.name
          }));
          $(child).children().last().on('click', {index:index}, createBookmark);
        }

        $('#folderDropdown'+index).append($('<a>', {
            class: 'dropdown-item',
            text: 'Create a Folder',
            'data-bs-toggle': 'modal',
            'data-bs-target': '#createFolderModal'
          }));
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  function loadSearchArticles() {
    let query = $('#searchInput').val();
      $.ajax({
        url: 'search_load_articles/',
        type: 'GET',
        data: {
          search: query
        },
        success: (data) => {
          let parent = $('#articles');
          $('#loadMoreButton').remove();
          $(parent).append(data.article_html);
        },
        error: (error) => {
          console.log(error);
        }
      });
  }

  function loadMoreArticles() {
    $.ajax({
      url: 'load_articles/',
      type: 'GET',
      headers: {
        'X-CSRFToken': '{{csrf_token}}'
      },
      success: (data) => {
        let parent = $('#articles');
        $('#loadMoreButton').remove();
        $(parent).append(data.article_html);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }