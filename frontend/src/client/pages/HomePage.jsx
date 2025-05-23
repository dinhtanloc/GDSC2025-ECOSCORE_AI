import React, {useState, useEffect} from "react";
import HeroSlider from "@client/components/UI/HeroSlider";
import Helmet from "@client/components/Helmet/Helmet";

import { Container, Row, Col, Form, FormGroup } from "reactstrap";
import AboutSection from "@client/components/UI/AboutSection";
import ServicesList from "@client/components/UI/ServicesList";
import BecomeOurCustomer from "@client/components/UI/BecomeOurCustomer";
import Testimonial from "@client/components/UI/Testimonial";
// import "@client/styles/find-car-form.css"
import BlogList from "@client/components/UI/BlogList";

const HomePage = () => {
  const [prompt, setPrompt] = useState('');
  const [color, setColor] = useState('');

  const handleFindCar = async (e) => {
    // e.preventDefault()
    // try {
    //   const combinedPrompt = color ? `${prompt} with ${color}`: prompt;
    //   const response = await instance.post('/categories/find-car/', {
    //     prompt: combinedPrompt,
    //   });
    //   const { products } = response.data;
    //   // Chuyển đến trang CarListing với dữ liệu được lọc
    //   navigate('/cars', { state: { products: products } });
    // } catch (error) {
    //   console.error('There was an error fetching the data!', error);
    // }
  };

  return (
    <Helmet title="Home">
      {/* ============= hero section =========== */}
      <section className="p-0 hero__slider-section">
        <HeroSlider />
      </section>
      {/* =========== about section ================ */}
      <AboutSection />
      {/* ========== services section ============ */}
      <section>
        <Container>
          <Row>
            <Col lg="12" className="mb-5 text-center">
              <h6 className="section__subtitle">See our</h6>
              <h2 className="section__title">Popular Services</h2>
            </Col>

            <ServicesList />
          </Row>
        </Container>
      </section>
      {/* =========== car offer section ============= */}
      <section>
        <Container>
          {/* <Row>
            <Col lg="12" className="text-center mb-5">
              <h6 className="section__subtitle">Come with</h6>
              <h2 className="section__title">Hot Offers</h2>
            </Col>

            {carData.slice(0, 6).map((item) => (
              <CarItem item={item} key={item.id} />
            ))}
          </Row> */}
        </Container>
      </section>
      {/* =========== become a driver section ============ */}
      <BecomeOurCustomer />

      {/* =========== testimonial section =========== */}
      <section>
        <Container>
          <div style={{marginBottom:'2%'}}></div>
          <Row>
            <Col lg="12" className="mb-4 text-center">
              <h6 className="section__subtitle">Our clients says</h6>
              <h2 className="section__title">Testimonials</h2>
            </Col>

            <Testimonial />
          </Row>
        </Container>
      </section>

      {/* =============== blog section =========== */}
      <section>
        <Container>
          <Row>
            <Col lg="12" className="mb-5 text-center">
              <h6 className="section__subtitle">Explore our blogs</h6>
              <h2 className="section__title">Latest Blogs</h2>
            </Col>

            <BlogList />
          </Row>
        </Container>
      </section>
    </Helmet>
  );
};

export default HomePage;
