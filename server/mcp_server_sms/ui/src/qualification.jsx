import React, { useMemo } from 'react';
import { QualificationController } from './qualification-controller.js';
import { QualificationWizard, QualificationErrorBoundary } from './qualification-wizard.jsx';

export function QualificationForm({ client, prefill }) {
  const controller = useMemo(() => new QualificationController(client, prefill), [client, prefill]);
  return <div className="qualification-wizard"><QualificationErrorBoundary>
    <QualificationWizard controller={controller} />
  </QualificationErrorBoundary></div>;
}
