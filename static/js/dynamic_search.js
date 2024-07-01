//  location Search.button: ./templates/partials/modal_search_post.html (line 22)

class Search {
  //  location Search.posts_endpoint : ./api/urls.py (line 12)
  static posts_endpoint = "/api/posts/?search=";

  //  location Search.button_trigger_modal : ./templates/partials/navbar.html (line 84)
  static button_trigger_modal = document.getElementById("search_button_trigger_modal");

  //  location Search.button: ./templates/partials/modal_search_post.html (line 22)
  static button = document.getElementById("search_button");

  //  location Search.input: ./templates/partials/modal_search_post.html (line 11)
  static input = document.getElementById("input_search");

  //  location Search.results_list: ./templates/partials/modal_search_post.html (line 14)
  static results_list = document.getElementById("results_list");

  // created in the Search.fill_the_results_list() method
  static result_items = document.getElementsByClassName("result_item");

  static async fetch_data_with_searched_value() {
    try {
      let searched_value = this.input.value;
      let response = await fetch(
        this.posts_endpoint + encodeURIComponent(searched_value)
      );
      let data = await response.json();

      return data;
    } catch (error) {
      console.error("Error fetching data :", error);
    }
  }

  static fill_the_results_list(fetched_data) {
    for (let i = 0; i < fetched_data.length; i++) {
      let title = fetched_data[i]["title"];
      results_list.innerHTML += `<a href="#" class="list-group-item list-group-item-action result_item">${title}</a>`;
    }
  }

  static select_item() {
    for (let i = 0; i < this.result_items.length; i++) {
      let result = this.result_items[i];

      result.addEventListener("click", (event) => {
        this.input.value = result.innerText;
        this.reset_results_list();
        this.validate_form();
        this.enable_search_button();
      });
    }
  }

  static reset_results_list() {
    this.results_list.innerHTML = null;
  }

  static reset_input_search() {
    this.input.value = null;
  }

  static validate_form() {
    this.input.classList.add("is-valid");
  }

  static reset_form_validation() {
    this.input.classList.remove("is-valid");
  }

  static disable_search_button() {
    this.button.classList.value = "btn btn-light disabled";
  }

  static enable_search_button() {
    this.button.classList.value = "btn btn-success";
  }

  static reset_search_form() {
    this.button_trigger_modal.addEventListener("click", (event) => {
      this.disable_search_button();
      this.reset_input_search();
      this.reset_form_validation();
      this.reset_results_list();
    });
  }

  static reset_start_search() {
    this.disable_search_button();
    this.reset_form_validation();
    this.reset_results_list();
  }

  static async start_search() {
    this.input.addEventListener("input", async (event) => {
      // 0. reset start search
      this.reset_start_search();

      // 1. get the searched value and fetch data
      let fetched_data = await this.fetch_data_with_searched_value();

      // 2. fill the results list with fetched data
      this.fill_the_results_list(fetched_data);

      // 3. select item from results list
      this.select_item();
    });
  }

  static async run() {
    this.reset_search_form();
    this.start_search();
  }
}

Search.run();
