package com.k12.mistake.notebook

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class MistakeNotebookApp : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
