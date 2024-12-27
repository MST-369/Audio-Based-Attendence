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

Below is a simplified workflow of the audio-based attendance process:

```mermaid
graph TD
    A[Professor's Laptop - Audio Input] --> B[Audio Recorded in Real-time]
    B --> C[Audio Submission to Database (Encrypted)]
    C --> D[Students Retrieve Audio After Submission]
    D --> E[Audio Comparison on Student Devices]
    E -- Match Found --> F[Attendance Marked]
    E -- No Match Found --> G[Attendance Denied]
    G --> H[Error Handling]
    F --> I[Dashboard Updated]

    subgraph Mitigating Proxy
        J[VPN Proxy Mitigation]
        K[Recorded vs Live Audio Detection]
        L[No ML/DL for Privacy]
    end
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
Email: [your-email@example.com](mailto:your-email@example.com)  
GitHub: [https://github.com/yourusername](https://github.com/yourusername)

---

## Acknowledgements

- Python community for amazing libraries.
- [Supabase](https://supabase.com/) for seamless database integration.
- Open-source contributors for speech recognition tools.
