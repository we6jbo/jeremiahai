#pragma once

#include <QMainWindow>
#include <QJsonObject>
#include <QList>
#include <QProcess>

class QLabel;
class QLineEdit;
class QTimer;
class QPlainTextEdit;
class QProgressBar;
class QSplitter;
class QScrollArea;
class QPushButton;
class QTabWidget;
class QTextEdit;
class QTreeWidget;
class QListWidget;
class QListWidgetItem;

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void writeVibeLauncher();
    void refreshFamilyView();

    void newWritingDocument();
    void openWritingDocument();
    void saveWritingDocument();
    void syncWritingDocuments();
    void analyzeWriting();
    void cancelWritingAnalysis();
    void readWritingAnalysisOutput();
    void writingAnalysisFinished(int exitCode, QProcess::ExitStatus exitStatus);
    void readWritingSyncOutput();
    void writingSyncFinished(int exitCode, QProcess::ExitStatus exitStatus);
    void writingIssueSelected(QListWidgetItem *item);
    void prepareWritingPortalDeployment();
    void prepareVibeWritingSupport();
    void reloadVibeDraft();
    void suggestWritingMetadata();
    void updateWritingClock();
    void runTroubleshootingAudit();
    void prepareTroubleshootingFix();
    void runIntegrityAudit();
    void refreshFileHistory();
    void fileHistorySelectionChanged();
    void deleteFileHistoryItem();
    void restoreFileHistoryItem();
    void previousFileVersion();
    void nextFileVersion();
    void restoreSelectedFileVersion();
    void openFileHistoryItem();
    void buildShareToChatGPT();
    void copyShareToChatGPT();
    void refreshBlogRuleFiles();
    void toggleSelectedBlogRule();
    void openBlogRulesFolder();
    void refreshThermaSimulatorNotes();
    void prepareThermaSimulatorVibe();
    void startBlogTimer();
    void stopBlogTimer();
    void resetBlogTimer();
    void saveBlogTimerNotes();
    void updateBlogTimerDisplay();
    void reloadFamilyData();
    void saveFamilyTroubleCopy();
    void prepareFamilyVibeTroubleshoot();

private:
    void buildTabs();
    QWidget *makeScrollableTab(QWidget *content, const QString &title);
    void ensureHomeData();
    QByteArray resourceBytes(const QString &path) const;
    QString writingCacheDir() const;
    QString currentWritingPath() const;
    QString slugify(const QString &text) const;
    QString suggestTitleFromBody(const QString &body) const;
    QString suggestFilenameFromDraft(const QString &title, const QString &body) const;
    QStringList suggestTagsFromBody(const QString &body) const;
    QString uniqueFilename(const QString &wanted) const;
    QString writingPolicyTime(const QDateTime &now, bool *visible = nullptr) const;
    void refreshWritingListStatus();
    QJsonObject fileHistoryCommand(const QStringList &args, bool *ok = nullptr);
    QString selectedHistoryFilename() const;
    QString collectEnabledBlogRules() const;
    QString latestVibeFinishedBody() const;
    QString sharePromptText() const;
    bool shareWindowActive() const;
    QString timerStatePath() const;
    int expectedBlogMinutes() const;
    qint64 currentBlogElapsedSeconds() const;
    void loadBlogTimerState();
    void persistBlogTimerState();
    QString timerContextText() const;
    QString familyMirrorPath() const;
    QString familyTroublePath() const;
    QString familyErrorsPath() const;
    bool loadKinMapState(QJsonObject *out, QString *sourceUsed, QString *errorText);
    void writeFamilyError(const QString &message, const QString &sourcePath);
    void setFamilyTroubleVisible(bool visible, const QString &message=QString());

    void clearWritingFeedback();
    void addWritingIssue(const QJsonObject &issue);
    void refreshWritingHighlights();
    void showWritingIssue(int index);
    QString formatWritingIssue(const QJsonObject &issue) const;

    Ui::MainWindow *ui;
    QTabWidget *tabs = nullptr;
    QTreeWidget *familyTree = nullptr;
    QTreeWidget *fileHistoryTree = nullptr;
    QLabel *familySummary = nullptr;
    QTextEdit *vibeStatus = nullptr;

    QLineEdit *writingTitle = nullptr;
    QLineEdit *writingFilename = nullptr;
    QLineEdit *writingAuthor = nullptr;
    QLineEdit *writingPublishDate = nullptr;
    QLineEdit *writingTags = nullptr;
    QWidget *blogDetailsContent = nullptr;
    QLabel *writingClock = nullptr;
    QTimer *writingClockTimer = nullptr;
    QPlainTextEdit *writingEditor = nullptr;
    QTextEdit *writingCoach = nullptr;
    QTextEdit *troubleshootingOutput = nullptr;
    QTextEdit *shareToChatGPTText = nullptr;
    QTextEdit *thermaSimulatorNotes = nullptr;
    QListWidget *writingIssues = nullptr;
    QListWidget *fileVersionList = nullptr;
    QListWidget *blogRuleList = nullptr;
    QLabel *writingStatus = nullptr;
    QLabel *writingQualityFlag = nullptr;
    QLabel *fileHistoryStatus = nullptr;
    QLabel *shareWindowStatus = nullptr;
    QLabel *thermaSimulatorStatus = nullptr;
    QLabel *timerElapsedLabel = nullptr;
    QLabel *timerBudgetLabel = nullptr;
    QLineEdit *timerExpectedMinutes = nullptr;
    QTextEdit *timerNotes = nullptr;
    QTextEdit *timerEventLog = nullptr;
    QTimer *blogTimerTick = nullptr;
    QDateTime blogTimerStartedAt;
    qint64 blogTimerAccumulatedSeconds = 0;
    bool blogTimerRunning = false;
    QWidget *familyTroubleTab = nullptr;
    QTextEdit *familyTroubleEditor = nullptr;
    QTextEdit *familyErrorView = nullptr;
    QString familyActiveSource;
    QProgressBar *writingProgress = nullptr;
    QPushButton *writingAnalyzeButton = nullptr;
    QPushButton *writingCancelButton = nullptr;
    QProcess *writingAnalysisProcess = nullptr;
    QProcess *writingSyncProcess = nullptr;
    QByteArray writingAnalysisBuffer;
    QByteArray writingSyncBuffer;
    QList<QJsonObject> writingIssueData;
    QString currentWritingFile;
};
