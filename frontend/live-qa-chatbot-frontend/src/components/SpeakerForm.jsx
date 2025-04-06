// src/components/SpeakerForm.js
import React, { useState } from "react";
import styles from "./SpeakerForm.module.css";

const SpeakerForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    title: "",
    description: "",
    document: null,
  });

  const [successMessage, setSuccessMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, document: e.target.files[0] });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!formData.name || !formData.title || !formData.description || !formData.document) {
      alert("Please fill in all fields and upload a document.");
      return;
    }

    // Simulate form submission
    setTimeout(() => {
      setSuccessMessage("Speaker details submitted successfully!");
      setFormData({
        name: "",
        title: "",
        description: "",
        document: null,
      });
    }, 1000);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Add Speaker Details</h1>
      {successMessage && <p className={styles.successMessage}>{successMessage}</p>}
      <form className={styles.form} onSubmit={handleSubmit}>
        <label className={styles.label}>
          Speaker Name
          <input
            className={styles.input}
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter speaker's name"
          />
        </label>

        <label className={styles.label}>
          Speech Title
          <input
            className={styles.input}
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Enter speech title"
          />
        </label>

        <label className={styles.label}>
          Description
          <textarea
            className={styles.textarea}
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Enter speech description"
          />
        </label>

        <label className={styles.label}>
          Upload Document
          <input
            className={styles.fileInput}
            type="file"
            name="document"
            onChange={handleFileChange}
          />
        </label>

        <button className={styles.submitButton} type="submit">
          Submit
        </button>
      </form>
    </div>
  );
};

export default SpeakerForm;
