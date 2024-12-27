# Audio-Based Attendance System

An innovative attendance system that uses voice recognition to mark attendance efficiently and securely. This project leverages audio processing and speech recognition to streamline the attendance process in classrooms, workplaces, or events.

---

## Features

- **Speech Recognition**: Converts spoken input into text to mark attendance.
- **Voice Authentication**: Validates identity using voice biometrics (optional).
- **Real-Time Processing**: Instantly logs attendance.
- **Secure Data Storage**: Stores attendance data in a database with encryption.
- **Accessible**: Suitable for visually impaired individuals or hands-free environments.

---

## Technology Stack

- **Programming Language**: Python
- **Audio Processing**: SpeechRecognition library, pyannote.audio
- **Database**: Supabase (PostgreSQL backend)
- **Frameworks**: Flask or Streamlit (for UI)
- **Cloud Services** (optional): Google Speech-to-Text, Azure Speech Services
- **Hardware**: Microphone or audio input device

---

## Workflow Diagram

Below is a GitHub-friendly textual representation of the workflow:

1. **Professor's Laptop**: Audio is recorded in real-time.
2. **Audio Submission**: The professor submits the audio to a secure database (encrypted).
3. **Students' Laptops**: Students retrieve the professor's audio after submission.
4. **Audio Comparison**: Comparison is performed locally on students' laptops between the live room audio and the submitted professor's audio.
   - **Match Found**: Attendance is marked.
   - **No Match Found**: Attendance is denied.
5. **Dashboard Update**: Attendance records are updated for both students and professors.

### Animated Workflow (Steps Visualization)

```ascii
+-------------------+
| Professor Laptop  |
| (Audio Recording) |
+-------------------+
        |
        v
+-------------------+
| Submit Audio to   |
| Database (Encrypt)|
+-------------------+
        |
        v
+-------------------+
| Students Retrieve |
| Audio for Local   |
| Comparison        |
+-------------------+
        |
        v
+-------------------+
| Compare Live Room |
| Audio with        |
| Submitted Audio   |
+-------------------+
     /       \
    v         v
+-------+   +--------+
| Match |   | No     |
| Found |   | Match  |
| Mark  |   | Deny   |
| Attend|   | Attend |
+-------+   +--------+
        |
        v
+-------------------+
| Dashboard Update |
+-------------------+
```

---

## How It Works

1. **Professor Audio Submission**: Professors record live audio on their laptops and submit it to the database, where it is stored in encrypted form.
2. **Student Audio Comparison**: Students retrieve the professor's submitted audio and compare it with live audio recorded on their local devices.
3. **Attendance Marking**: Attendance is marked based on the audio comparison result.
4. **Proxy Mitigation**:
   - VPN proxies are detected and mitigated.
   - Sharing pre-recorded audio is ineffective as live audio differences are detectable.
   - The system ensures privacy without using ML/DL models or biometric data.

---

## Future Enhancements

- Support for multiple languages and accents.
- Noise-cancellation for improved accuracy.
- Mobile application for remote attendance.
- Analytics dashboard for attendance trends.

---

## Contributing

Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes and push:
   ```bash
   git commit -m "Add feature name"
   git push origin feature-name
   ```
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

**Mani Surya Teja**  
Email: [msurya@example.com](mailto:msurya@example.com)  
GitHub: [https://github.com/manisurya](https://github.com/manisurya)

---

## Acknowledgements

- Python community for amazing libraries.
- [Supabase](https://supabase.com/) for seamless database integration.
- Open-source contributors for speech recognition tools.
