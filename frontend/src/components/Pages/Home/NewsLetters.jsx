import { Link } from "react-router-dom";
import {
  card,
  card1,
  card2,
  card3,
  card4,
  card5,
} from "../../../assets/images";

const NewsLetters = () => {
  const images = [card, card1, card2, card3, card4, card5];

  return (
    <div className="bg-gray-100">
      <div className="max-w-screen-2xl container py-12 xl:px-28 px-4 pb-12">
        <p className="title">Follow Products And Discounts on Instagram</p>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4 mt-8">
          {images.map((image, index) => (
            <Link to="/" key={index}>
              <img
                src={image}
                alt={`Card ${index + 1}`}
                className="w-full h-auto"
              />
            </Link>
          ))}
        </div>
        <div className="flex flex-col mt-3 gap-10 justify-center items-center">
          <p className="title">Or Subscribe to the newsletter</p>
          <div className="flex flex-col w-full md:flex-row gap-5 md:w-[40%]">
            <input
              type="text"
              placeholder="Enter your text"
              className="border-b-2 border-gray-400 focus:border-black outline-none px-4 py-2 w-full bg-transparent font-serif"
            />
            <button className="border-b-2 text-sm px-3 border-gray-400 font-bold transition duration-300 hover:border-black hover:text-black inline-block uppercase text-gray-500">
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewsLetters;