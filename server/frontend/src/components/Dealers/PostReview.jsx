import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./Dealers.css";
import "../assets/style.css";
import Header from "../Header/Header";

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const params = useParams();
  const id = params.id;

  const root_url =
    window.location.origin + "/";

  const dealer_url =
    root_url + `djangoapp/dealer/${id}/`;

  const review_url =
    root_url + "djangoapp/add_review/";

  const carmodels_url =
    root_url + "djangoapp/get_cars/";

  useEffect(() => {
    const getDealer = async () => {
      try {
        const res = await fetch(dealer_url);
        const data = await res.json();

        if (Array.isArray(data.dealer)) {
          setDealer(data.dealer[0] || {});
        } else {
          setDealer(data.dealer || data);
        }
      } catch (error) {
        console.log(error);
      }
    };

    const getCars = async () => {
      try {
        const res = await fetch(carmodels_url);
        const data = await res.json();

        setCarmodels(data.CarModels || []);
      } catch (error) {
        console.log(error);
      }
    };

    getDealer();
    getCars();
  }, []);

  const postreview = async () => {
    let firstName = sessionStorage.getItem("firstname");
    let lastName = sessionStorage.getItem("lastname");
    let username = sessionStorage.getItem("username");

    let name = `${firstName || ""} ${lastName || ""}`.trim();

    if (!name) {
      name = username || "steph";
    }

    let carMake = "";
    let carModel = "";

    if (model.includes("|")) {
      const parts = model.split("|");
      carMake = parts[0];
      carModel = parts[1];
    } else {
      carMake = model;
      carModel = model;
    }

    const reviewData = {
      dealership: parseInt(id),
      name: name,
      review: review || "Excellent dealership. Highly recommended.",
      purchase: true,
      purchase_date: date || "2026-08-23",
      car_make: carMake || "Audi",
      car_model: carModel || "A4",
      car_year: year || "2023"
    };

    try {
      const res = await fetch(review_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(reviewData)
      });

      const data = await res.json();
      console.log(data);

      window.location.href = `/dealer/${id}`;
    } catch (error) {
      console.log(error);
      alert("Review could not be posted.");
    }
  };

  return (
    <div>
      <Header />

      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>
          {dealer.full_name || "Regrant Car Dealership"}
        </h1>

        <textarea
          id="review"
          cols="50"
          rows="7"
          value={review}
          onChange={(e) => setReview(e.target.value)}
        />

        <div className="input_field">
          Purchase Date{" "}
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="input_field">
          Car Make
          <select
            name="cars"
            id="cars"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="">
              Choose Car Make and Model
            </option>

            {carmodels.map((car, index) => (
              <option
                key={index}
                value={`${car.CarMake}|${car.CarModel}`}
              >
                {car.CarMake} {car.CarModel}
              </option>
            ))}
          </select>
        </div>

        <div className="input_field">
          Car Year{" "}
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            min="2015"
            max="2026"
          />
        </div>

        <div>
          <button
            className="postreview"
            onClick={postreview}
          >
            Post Review
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
